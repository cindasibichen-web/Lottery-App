from rest_framework.views import APIView
from rest_framework.response import Response
from lottery_app.models import Lottery
from lottery_app.serializers import LotterySerializer
# from rest_framework.authentication import IsAuthenticated
from rest_framework.permissions import IsAuthenticated 
from lottery_app.serializers import *
from rest_framework import status
from lottery_web_app.serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
from django.http import JsonResponse
from datetime import datetime, timedelta
import pytz
from lottery_app.utils.transit_encryption import  *
from lottery_app.middleware.encryption_middleware import *



# list all advertisment 
class ActiveAdvertisementListView(APIView):
   

    def get(self, request):
        ads = Advertisement.objects.filter(is_active=True).order_by('-created_at')
        serializer = AdvertisementSerializer(ads, many=True, context={'request': request})
        
        # Return success=true if data found, else success=false with empty list
        if serializer.data:
            response =  Response(
                {"success": True, "data": serializer.data},
                status=status.HTTP_200_OK
            )
            response.encrypt_payload = True
            return response
        else:
            response =  Response(
                {"success": False, "data": [], "message": "No active advertisements found."},
                status=status.HTTP_200_OK
            )
            response.encrypt_payload = True
            return response
        