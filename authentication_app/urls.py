from django.urls import path 
from . views import *

urlpatterns = [
   
   path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
   path('login/', UserLoginAPIView.as_view(), name='user-login'),
   path("send-otp/", SendOTPAPIView.as_view(), name="send_otp"),
   path("verify-otp/", VerifyOTPAPIView.as_view(), name="verify_otp"),
   path("reset-password/", ResetPasswordAPIView.as_view(), name="reset_password"),
   path('user-logout/',UserLogoutApi.as_view(),name='user-logout'),
]