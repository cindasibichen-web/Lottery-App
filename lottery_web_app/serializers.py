from rest_framework import serializers
from  lottery_app.models import *


class AdvertisementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)  
    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ['created_at','created_by','is_active']


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'        


class LotteryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotteryInfo
        fields = "__all__"  
        
class AccountSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountSupport
        fields = "__all__" 
        
class Weekly_ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklySchedule
        fields = "__all__"        
        
        
class ImportantRule_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantRule
        fields = "__all__"    
        
class SafetyRule_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyRule
        fields = "__all__"   
        
        
class OfficialResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialResource
        fields = '__all__'    
        
        
        
class GeneralHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralHelp
        fields = "__all__"       
        
        
class AccountsupporthelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = accountsupporthelp
        fields = "__all__"   
        
class paymentandsubscriptionhelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = paymentandsubscriptionhelp
        fields = "__all__"     
        
        
              
class PurchaseLotteryHelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchaselotteryhelp
        fields = "__all__"        