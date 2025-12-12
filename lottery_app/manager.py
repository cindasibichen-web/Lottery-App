from django.contrib.auth.models import BaseUserManager
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone_number, role="User", password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(phone_number=phone_number, role=role, **extra_fields)
        if password:
            user.set_password(password)  
        else:
            user.set_unusable_password()  

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            phone_number=phone_number,
            role="SuperAdmin",
            password=password,
            **extra_fields
        )
