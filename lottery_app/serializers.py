from rest_framework import serializers
from . models import *
from .translation import *


# lottery serializer with translation support
class LotterySerializer(serializers.ModelSerializer):
    lottery_name_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Lottery
        fields = [
            'id',
            'lottery_name',       # writable
            'draw_date',
            'status',             # writable
            'logo',
            'ticket_rupees',
            'ticket_number',
            'created_by',
            'created_at',
            'lottery_name_display',
            'status_display',
        ]
        read_only_fields = ['created_by', 'created_at']

    def get_lottery_name_display(self, obj):
        lang = self.context.get('lang', 'en')
        return transliterate_text(obj.lottery_name, lang)

    def get_status_display(self, obj):
        lang = self.context.get('lang', 'en')
        return transliterate_text(obj.status, lang)



# user profile get api 
class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    profile = serializers.ImageField(source='profile_picture', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'full_name', 'email', 'phone_number', 'location','role', 'date_joined', 'profile','blood_group','city','state','pincode','nationality','job_title','job_field','nominee_other_details','nominee_name','nominee_phone_number','district','address','profile_picture']




# lucky number serializer 
class LuckyNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersLuckyNumber
        fields = ['id', 'number', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user_profile = self.context['request'].user.userprofile  # Get logged-in user’s profile
        return UsersLuckyNumber.objects.create(user=user_profile, **validated_data)
    

from decimal import Decimal    
class CartItemSerializer(serializers.ModelSerializer):
    lottery_name = serializers.CharField(source="lottery.lottery_name", read_only=True)
    ticket_price = serializers.SerializerMethodField()
    ticket_number = serializers.CharField(source="lottery.ticket_number", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "lottery",
            "lottery_name",
            "ticket_price",
            "quantity",
            "ticket_number",
            "total_price",
        ]

    def get_ticket_price(self, obj):
        """Convert encrypted string to Decimal"""
        try:
            return str(Decimal(obj.lottery.ticket_rupees or "0"))
        except:
            return "0.00"

    def get_total_price(self, obj):
        """Correct multiplication"""
        try:
            price = Decimal(obj.lottery.ticket_rupees or "0")
        except:
            price = Decimal("0")

        total = price * obj.quantity
        return str(total)






class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    def get_grand_total(self, obj):
        total = Decimal("0.00")
        for item in obj.items.all():
            price = Decimal(item.lottery.ticket_rupees or "0")
            total += price * item.quantity
        return str(total)    
    

#  price claim rules serializer
class  PriceClaimRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceClaimRule
        fields = '__all__' 


class DocumentsRequiredSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsRequiredForPrizeClaim
        fields = '__all__'


class ImportentRemindersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportentReminders
        fields = '__all__'        



class ContactSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSupport
        fields = "__all__"
class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = '__all__'        


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'                