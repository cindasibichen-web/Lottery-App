from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from lottery_app.sms_service import *
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from lottery_app.utils.transit_encryption import *
import json


# Create your views here.
class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        print(request.data) 
        decrypted_data = decrypt_request_payload(request)

        if decrypted_data:
            print(decrypted_data)
            # Replace request.data with decrypted version
            data = decrypted_data
        else:
            print(request.data)
            data = request.data
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response =  Response(
                {
                    "success": True,
                    "message": "User registered successfully",
                },
                status=status.HTTP_201_CREATED
            )
            response.encrypt_payload = True      
            return response
        response =  Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        response.encrypt_payload = True      
        return response
    



#login         
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login using phone number and password (encrypted or normal)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'encrypted_key': openapi.Schema(type=openapi.TYPE_STRING),
                'cipher': openapi.Schema(type=openapi.TYPE_STRING),
                'nonce': openapi.Schema(type=openapi.TYPE_STRING),
                'tag': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        security=[]
    )
    def post(self, request):

        encrypted_key = request.data.get("encrypted_key")
        cipher = request.data.get("cipher")
        nonce = request.data.get("nonce")
        tag = request.data.get("tag")

        # ------------------------------------------------------------------
        # CASE 1: IF RSA + AES ENCRYPTED PAYLOAD IS PROVIDED
        # ------------------------------------------------------------------
        if encrypted_key and cipher and nonce and tag:
            try:
                aes_key = rsa_decrypt_key(encrypted_key)
                decrypted_json = aes_decrypt(cipher, nonce, tag, aes_key)
                login_data = json.loads(decrypted_json)

                phone_number = login_data.get("phone_number")
                password = login_data.get("password")

            except Exception as e:
                return Response(
                    {"success": False, "message": "Invalid encrypted payload"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # ------------------------------------------------------------------
        # CASE 2: NORMAL LOGIN (NO ENCRYPTION FROM FLUTTER)
        # ------------------------------------------------------------------
        else:
            phone_number = request.data.get("phone_number")
            password = request.data.get("password")

        # Validate
        if not phone_number or not password:
            return Response(
                {"success": False, "message": "Phone number and password required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate
        user = authenticate(request, phone_number=phone_number, password=password)

        if user is None:
            return Response(
                {"success": False, "message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        refresh["role"] = user.role
        refresh["user_id"] = user.id

        return Response(
            {
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK
        )


# send otp
class SendOTPAPIView(APIView):
    permission_classes = [AllowAny]
    """Send OTP to user's registered phone number"""

    def post(self, request):
        print(request.data) 
        decrypted_data = decrypt_request_payload(request)

        if decrypted_data:
            print(decrypted_data)
            # Replace request.data with decrypted version
            data = decrypted_data
        else:
            print(request.data)
            data = request.data
        phone = data.get("phone")
        if not phone:
            response =  Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
            response.encrypt_payload = True      
            return response


        try:
            user = User.objects.get(phone_number=phone)  # assuming phone stored in Profile model
        except User.DoesNotExist:
            return Response({"error": "No account associated with this phone number."}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP
        otp = generate_otp()

        # Save OTP (with expiry)
        OTPVerification.objects.create(
            user=user,
            otp=otp,
            expires_at=timezone.now() + timedelta(seconds=60),
        )

        # Send SMS
        sms_response = send_otp_via_twilio(phone, otp)

        if sms_response.get("return", False):
            response = Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
            response.encrypt_payload = True      
            return response
        else:
            response =  Response({"error": "Failed to send OTP", "details": sms_response}, status=status.HTTP_400_BAD_REQUEST)
            response.encrypt_payload = True      
            return response
        
# verify otp
class VerifyOTPAPIView(APIView):
    permission_classes = [AllowAny]
    """Verify OTP for password reset"""

    def post(self, request):
        print(request.data) 
        decrypted_data = decrypt_request_payload(request)

        if decrypted_data:
            print(decrypted_data)
           
            data = decrypted_data
        else:
            print(request.data)
            data = request.data
        phone = data.get("phone")
        otp = data.get("otp")

        try:
            user = User.objects.get(profile__phone=phone)
        except User.DoesNotExist:
            response =  Response({"error": "Invalid phone number"}, status=status.HTTP_404_NOT_FOUND)
            response.encrypt_payload = True      
            return response

        otp_obj = OTPVerification.objects.filter(user=user).last()
        if not otp_obj or not otp_obj.is_valid(otp):
            response = Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
            response.encrypt_payload = True      
            return response



        response = Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        response.encrypt_payload = True      
        return response




# reset password
class ResetPasswordAPIView(APIView):
    permission_classes = [AllowAny]
    """Reset password after OTP verification"""

    def post(self, request):
        print(request.data) 
        decrypted_data = decrypt_request_payload(request)

        if decrypted_data:
            print(decrypted_data)
           
            data = decrypted_data
        else:
            print(request.data)
            data = request.data
        phone = data.get("phone_number")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if not all([phone, new_password, confirm_password]):
            response =  Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
            response.encrypt_payload = True      
            return response

        if new_password != confirm_password:
            response = Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            response.encrypt_payload = True      
            return response

        # Get user

        try:
            user_profile = UserProfile.objects.get(user__phone_number=phone)
            user = user_profile.user
        except UserProfile.DoesNotExist:
            response = Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            response.encrypt_payload = True      
            return response


        otp_obj = OTPVerification.objects.filter(user=user).last()
        if not otp_obj or otp_obj.expires_at < timezone.now():
            response = Response({"error": "OTP verification expired. Please request again."}, status=status.HTTP_400_BAD_REQUEST)
            response.encrypt_payload = True      
            return response


        # Update password
        user.password = make_password(new_password)
        user.save()

        # Delete OTP after use
        OTPVerification.objects.filter(user=user).delete()

        response =  Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        response.encrypt_payload = True      
        return response




# logout api
class UserLogoutApi(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.data) 
        decrypted_data = decrypt_request_payload(request)

        if decrypted_data:
            print(decrypted_data)
            
            data = decrypted_data
        else:
            print(request.data)
            data = request.data
        refresh_token = data.get("refresh")

        if not refresh_token:
            response =  Response(
                {"success": False, "message": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
            response.encrypt_payload = True      
            return response


        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  
            response =  Response(
                {"success": True, "message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )
            response.encrypt_payload = True      
            return response
        except TokenError:
            response = Response(
                {"success": False, "message": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )
            response.encrypt_payload = True      
            return response