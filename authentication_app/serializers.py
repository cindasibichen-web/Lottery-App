from rest_framework import serializers
from lottery_app.models import *




class UserRegistrationSerializer(serializers.Serializer):

    role = serializers.ChoiceField(choices=['User', 'Dealer'],default='User')
    full_name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255 , required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)
    profile_picture = serializers.ImageField(required=False)
    email = serializers.EmailField(required=False)
    confirm_password = serializers.CharField(write_only=True)

    # Profile-related fields
    blood_group = serializers.CharField(max_length=100, required=False, allow_blank=True)
    city = serializers.CharField(max_length=300, required=False, allow_blank=True)
    state = serializers.CharField(max_length=300, required=False, allow_blank=True)
    pincode = serializers.CharField(max_length=10, required=False, allow_blank=True)
    nationality = serializers.CharField(max_length=200, required=False, allow_blank=True)
    job_title = serializers.CharField(max_length=300, required=False, allow_blank=True)
    job_field = serializers.CharField(max_length=300, required=False, allow_blank=True)
    nominee_other_details = serializers.CharField(required=False, allow_blank=True)
    nominee_name = serializers.CharField(max_length=300, required=False, allow_blank=True)
    nominee_phone_number = serializers.CharField(max_length=400, required=False, allow_blank=True)
    district = serializers.CharField(max_length=300, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)

    agency_name = serializers.CharField(required=False)
    owner_name = serializers.CharField(required=False)
    contact_number = serializers.CharField(required=False)
    id_documents = serializers.FileField(required=False)
    dob = serializers.DateField(required=False)
    license_expiry_date = serializers.DateField(required=False)
    registration_number = serializers.CharField(required=False)
    registration_date = serializers.DateField(required=False)


    def validate(self, data):
        # Password confirmation check
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        # Check for existing phone number
        if User.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError("Phone number already registered.")

        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        role = validated_data.get('role', 'User')

        # Common user fields
        full_name = validated_data.get('full_name')
        phone_number = validated_data.get('phone_number')
        email = validated_data.get('email', None)
        password = validated_data.get('password')

        # Create base user first
        user = User.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            role=role
        )
        user.set_password(password)
        user.save()

        # -----------------------------
        # USER PROFILE CREATION
        # -----------------------------
        if role == "User":
            profile_fields = {
                key: validated_data.get(key)
                for key in [
                    "full_name", "location", "blood_group", "city", "state",
                    "pincode", "nationality", "job_title", "job_field",
                    "nominee_other_details", "nominee_name", "nominee_phone_number",
                    "district", "address", "profile_picture"
                ]
            }
            UserProfile.objects.create(user=user, **profile_fields)

        # -----------------------------
        # DEALER PROFILE CREATION
        # -----------------------------
        if role == "Dealer":
            dealer_fields = {
                "agency_name": validated_data.get("agency_name"),
                "owner_name": validated_data.get("full_name"),
                "contact_number": validated_data.get("phone_number"),
                "email": validated_data.get("email"),
                "address": validated_data.get("address"),
                "state": validated_data.get("state"),
                "city": validated_data.get("city"),
                "pincode": validated_data.get("pincode"),
                "dob": validated_data.get("dob"),
                "license_expiry_date": validated_data.get("license_expiry_date"),
                "registration_number": validated_data.get("registration_number"),
                "registration_date": validated_data.get("registration_date"),
                "id_documents": validated_data.get("id_documents"),
                "profile_picture": validated_data.get("profile_picture"),
            }

            DealerProfile.objects.create(user=user, **dealer_fields)

        return user


    # def create(self, validated_data):
    #     # Remove confirm_password (not needed for creation)
    #     validated_data.pop('confirm_password')

    #     # Extract user fields
    #     full_name = validated_data.get('full_name')
    #     phone_number = validated_data.get('phone_number')
    #     email = validated_data.get('email', None)
    #     password = validated_data.get('password')

    #     # Extract profile fields separately
    #     profile_fields = {
    #         key: validated_data.get(key)
    #         for key in [
    #             "full_name", "location", "blood_group", "city", "state",
    #             "pincode", "nationality", "job_title", "job_field",
    #             "nominee_other_details", "nominee_name", "nominee_phone_number",
    #             "district", "address", "profile_picture"
    #         ]
    #     }

    #     # Create user
    #     user = User.objects.create(
    #         full_name=full_name,
    #         phone_number=phone_number,
    #         email=email,
    #     )
    #     user.set_password(password)
    #     user.save()

    #     # Create linked profile
    #     UserProfile.objects.create(user=user, **profile_fields)

    #     return user