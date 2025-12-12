from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from lottery_app.models import *
from lottery_app.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework import status
from lottery_web_app.serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from lottery_app.utils.transit_encryption import  *
from lottery_app.middleware.encryption_middleware import *



#add advertisment  api  
class AdvertisementCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Create a new advertisement entry. Requires authentication.",
        request_body=AdvertisementSerializer,
        manual_parameters=[
            openapi.Parameter(
                name='Content-Type',
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=False,
                description="Use multipart/form-data for image upload",
                default="multipart/form-data"
            )
        ],
        consumes=['multipart/form-data'], 
        responses={
            201: openapi.Response(description="Advertisement created successfully"),
            400: openapi.Response(description="Validation Error"),
            401: openapi.Response(description="Authentication credentials were not provided or invalid."),
        },
    )

    def post(self, request):
        # print(request.data) 
        # decrypted_data = decrypt_request_payload(request)

        # if decrypted_data:
        #     print(decrypted_data)
        #     # Replace request.data with decrypted version
        #     data = decrypted_data
        # else:
        #     print(request.data)
        #     data = request.data
        serializer = AdvertisementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user.userprofile)
            return Response({
                "success": True,
                "message": "Advertisement created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

# update advertisment api
class AdvertisementUpdateAPIView(APIView):
    """
    Update an existing advertisement entry (Authenticated Admin only).
    """
    permission_classes = [IsAuthenticated]

   
    @swagger_auto_schema(
        operation_description="Update an existing advertisement entry. Requires authentication.",
        request_body=AdvertisementSerializer,
        consumes=['multipart/form-data'],
        responses={
            200: openapi.Response(description="Advertisement updated successfully"),
            400: openapi.Response(description="Validation Error"),
            404: openapi.Response(description="Advertisement not found."),
        },
    )
    def patch(self, request, pk):
        try:
            advertisement = Advertisement.objects.get(pk=pk, created_by=request.user.userprofile)
        except Advertisement.DoesNotExist:
            return Response({
                "success": False,
                "message": "Advertisement not found or you do not have permission to edit it."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AdvertisementSerializer(advertisement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Advertisement partially updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# delete advertisment api 
class AdvertisementDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Deleted a advertisement entry. Requires authentication.",
        responses={
            201: openapi.Response(description="Advertisement Deleted successfully"),
            400: openapi.Response(description="Validation Error"),
            401: openapi.Response(description="Authentication credentials were not provided or invalid."),
        },
    )

    def delete(self, request, advertisement_id):
        try:
            # Ensure the advertisement belongs to the logged-in user
            advertisement = Advertisement.objects.get(id=advertisement_id, created_by=request.user.userprofile)
        except Advertisement.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Advertisement not found or you don't have permission to delete it."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the advertisement
        advertisement.delete()
        return Response(
            {
                "success": True,
                "message": "Advertisement deleted successfully."
            },
            status=status.HTTP_200_OK
        ) 