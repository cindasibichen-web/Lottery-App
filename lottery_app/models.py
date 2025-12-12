from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from lottery_app.utils.encrypt_decrypt_data import *



# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('SuperAdmin', 'SuperAdmin'),
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Dealer', 'Dealer'),   
    )
    full_name = EncryptedCharField(max_length=600)
    email = EncryptedEmailField()
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=600, choices=ROLE_CHOICES, default='User')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'  
    REQUIRED_FIELDS = []  

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
    

# main user profile model 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = EncryptedCharField(max_length=600)
    location = EncryptedCharField(max_length=600)
    blood_group = EncryptedCharField(max_length=100, blank=True, null=True)
    city = EncryptedCharField(max_length=300, blank=True, null=True)
    state = EncryptedCharField(max_length=300, blank=True, null=True)
    pincode = EncryptedCharField(max_length=300, blank=True, null=True)
    nationality = EncryptedCharField(max_length=200, blank=True, null=True)
    job_title = EncryptedCharField(max_length=300, blank=True, null=True)
    job_field = EncryptedCharField(max_length=300, blank=True, null=True)
    nominee_other_details = EncryptedTextField(blank=True, null=True)
    nominee_name = EncryptedCharField(max_length=300, blank=True, null=True)
    nominee_phone_number = EncryptedCharField(max_length=400,null=True,blank=True)
    district = EncryptedCharField(max_length=300, blank=True, null=True)
    address = EncryptedTextField(blank=True, null=True)
    profile_picture = EncryptedImageField(upload_to='profile_pictures/', blank=True, null=True,max_length=700)


    def __str__(self):
        return self.full_name
    
    
# dealer profile model
class DealerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agency_name = EncryptedCharField(max_length=600)
    owner_name = EncryptedCharField(max_length=600)
    contact_number = EncryptedCharField(max_length=200)
    address = EncryptedTextField(blank=True, null=True)
    city = EncryptedCharField(max_length=300, blank=True, null=True)
    email = EncryptedEmailField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    license_expiry_date = models.DateField(blank=True, null=True)
    id_documents = models.FileField(upload_to='dealer_id_documents/', blank=True, null=True,max_length=700)
    state = EncryptedCharField(max_length=300, blank=True, null=True)
    pincode = EncryptedCharField(max_length=300, blank=True, null=True)
    registration_number = EncryptedCharField(max_length=400, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='dealer_profile_pictures/', blank=True, null=True,max_length=700)

    def __str__(self):
        return f"{self.owner_name} - {self.agency_name}"



class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = EncryptedCharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self, otp):
        from django.utils import timezone
        return self.otp == otp and timezone.now() <= self.expires_at


# lottery table
class Lottery(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('upcoming', 'Upcoming'),
    ]


    lottery_name = EncryptedCharField(max_length=300)
    ticket_rupees = EncryptedCharField(max_length=300,null=True,blank=True)
    ticket_number = EncryptedCharField(max_length=300,blank=True, null=True)
    draw_date = models.DateField()
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='lotteries'
    )
    status = EncryptedCharField(max_length=100, choices=STATUS_CHOICES)
    logo = models.ImageField(upload_to='lottery_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lottery_name} ({self.status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Lottery"
        verbose_name_plural = "Lotteries"



# Prize Model
class Prize(models.Model):
   
    lottery = models.ForeignKey(Lottery,on_delete=models.CASCADE,related_name='prizes' )
    prize_name = EncryptedCharField( max_length=400,blank=True,null=True,help_text="e.g.,'1st Prize', '2nd Prize'")
    prize_amount = EncryptedDecimalField(max_digits=12,decimal_places=2,blank=True,null=True,help_text="Amount of the prize")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prize_name or 'Prize'} - ₹{self.prize_amount or 0} ({self.lottery.lottery_name})"

    class Meta:
        ordering = ['id']
        verbose_name = "Prize"
        verbose_name_plural = "Prizes"   



# RESULT MODEL
# ------------------------------
class Result(models.Model):
    

    lottery = models.ForeignKey(Lottery,on_delete=models.CASCADE,related_name='results',help_text="Related lottery",null=True,blank=True)
    lottery_name = EncryptedCharField(max_length=400,help_text="Name of the lottery",null=True,blank=True)
    prize = models.ForeignKey(Prize,on_delete=models.CASCADE,related_name='results',help_text="Related prize",null=True,blank=True)
    winning_number = EncryptedCharField(max_length=200,help_text="Winning number for this prize")
    prizes = models.JSONField(default=dict,null=True,blank=True,help_text="Additional prize details in JSON format")
    location = EncryptedCharField(max_length=500,blank=True,null=True, help_text="e.g., 'Thiruvananthapuram'")
    result_date = models.DateTimeField(default=timezone.now,help_text="Date and time the result was announced")
    uploaded_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True,related_name='uploaded_results',help_text="Admin who uploaded this result")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lottery_name} - ({self.winning_number})"

    class Meta:
        ordering = ['-result_date']
        verbose_name = "Lottery Result"
        verbose_name_plural = "Lottery Results"        
        
        
        
# PREDICTION MODEL
# ------------------------------
class Prediction(models.Model):
    PLAN_CHOICES = [
        ('Plan 1', 'Plan 1'),
        ('Plan 2', 'Plan 2'),
        ('Plan 3', 'Plan 3'),
    ]

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='predictions',help_text="Who made the prediction")
    lottery = models.ForeignKey(Lottery,on_delete=models.CASCADE,related_name='predictions',help_text="Related lottery")
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE,related_name='predictions',help_text="Related prize")
    plan_type = EncryptedCharField(max_length=400,choices=PLAN_CHOICES,help_text="Prediction plan type")
    predicted_numbers = models.JSONField(help_text="List of numbers predicted")
    prediction_date = models.DateTimeField(auto_now_add=True)
    accuracy_score = models.FloatField(default=0, help_text="Accuracy from ML model (if available)")

    def __str__(self):
        return f"{self.user.full_name} - {self.lottery.lottery_name} ({self.plan_type})"

    class Meta:
        ordering = ['-prediction_date']
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"



# plans subscription model 
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Elite', 'Elite'),
    ]

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='subscriptions',help_text="Subscribed user")
    plan_name = EncryptedCharField(max_length=500,choices=PLAN_CHOICES,help_text='e.g., "Basic", "Premium", "Elite"')
    price = EncryptedCharField(max_length=500,help_text="Subscription price")
    start_date = models.DateTimeField(help_text="Subscription start date")
    end_date = EncryptedDateField(help_text="Subscription end date")
    is_active = models.BooleanField(default=True,help_text="Subscription active or not")
    created_at = models.DateTimeField(auto_now_add=True,help_text="Created timestamp")

    def __str__(self):
        return f"{self.user.full_name} - {self.plan_name} ({'Active' if self.is_active else 'Inactive'})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"        

# shopping cart model
class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.phone_number}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    lottery = models.ForeignKey(
        Lottery,
        on_delete=models.CASCADE
    )
   # ticket_number = EncryptedCharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
   #$ price = models.DecimalField(max_digits=10, decimal_places=2)  # ₹40

    def __str__(self):
        return f"{self.lottery.lottery_name}"



class SubscriptionPlan(models.Model):
    PLAN_LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('pro', 'Pro'),
    ]

    name = EncryptedCharField(max_length=300, choices=PLAN_LEVEL_CHOICES, default='basic')
    title = EncryptedCharField(max_length=500, default="Basic")
    description = EncryptedTextField(default="Get started with basic predictions")
    price = EncryptedCharField(max_length=400, default="99.00") 
    duration_in_months = models.PositiveIntegerField(default=1)
    predictions_per_month = models.PositiveIntegerField(default=10)

    prizes_included = EncryptedTextField(max_length=255, default="7th, 8th & 9th Prizes Only")
    numbers_per_prediction = models.PositiveIntegerField(default=15)
    show_prediction_percentage = models.BooleanField(default=True)
    low_risk_prediction = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} Plan - ${self.price}/month"
    
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Net Banking', 'Net Banking'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='payments',help_text="Paying user")
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE,related_name='payments',help_text="Linked subscription")
    amount = EncryptedDecimalField(max_digits=10,decimal_places=2,help_text="Paid amount")
    payment_method = EncryptedCharField(max_length=500,choices=PAYMENT_METHOD_CHOICES,help_text="Payment method type")
    transaction_id = EncryptedCharField(max_length=500,unique=True,help_text="Unique transaction reference")
    payment_status = EncryptedCharField(max_length=200,choices=PAYMENT_STATUS_CHOICES,default='Pending',help_text="Payment status")
    created_at = models.DateTimeField(auto_now_add=True,help_text="Payment time")

    def __str__(self):
        return f"{self.user.full_name} - ₹{self.amount} ({self.payment_status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"        



class Advertisement(models.Model):
    title = EncryptedCharField(max_length=500, help_text="Ad title")
    image = models.ImageField(upload_to='ads/', help_text="Ad image")
    redirect_url = EncryptedURLField(null=True, blank=True, help_text="Optional link when ad is clicked")
    is_active = models.BooleanField(default=True, help_text="Whether the ad is currently active")
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        limit_choices_to={'user__role': 'Admin'},
        related_name='advertisements',
        help_text="Admin who uploaded this advertisement"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when created")

    def __str__(self):
        return self.title
        
        
class Notification(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True,related_name='notifications',help_text="Target user (null = broadcast to all)")
    title = EncryptedCharField(max_length=700,help_text="Notification title")
    message = EncryptedTextField(help_text="Notification message content")
    is_read = models.BooleanField(default=False,help_text="Whether the notification has been read")
    created_at = models.DateTimeField(auto_now_add=True,help_text="Timestamp when notification was created")

    def __str__(self):
        target = self.user.full_name if self.user else "Broadcast"
        return f"{target} - {self.title})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"




#   lucky number saving table 
class UsersLuckyNumber(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='lucky_numbers',help_text="User associated with this lucky number")
    number = EncryptedCharField(max_length=100,help_text="The lucky number")
    created_at = models.DateTimeField(auto_now_add=True,help_text="Timestamp when the lucky number was created")

    def __str__(self):
        return f"{self.user.full_name} -- {self.number}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Lucky Number"
        verbose_name_plural = "Lucky Numbers"


#  basic rules for price claim
class PriceClaimRule(models.Model):
    title = EncryptedCharField(max_length=500, help_text="Rule title")
    description = EncryptedTextField(help_text="Detailed description of the rule")
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    


class DocumentsRequiredForPrizeClaim(models.Model):
    document_name = EncryptedCharField(max_length=500, help_text="Name of the required document")
    description = EncryptedTextField(help_text="Description or details about the document",null=True,blank=True)
    is_mandatory = models.BooleanField(default=True, help_text="Whether this document is mandatory for prize claim")

    def __str__(self):
        return self.document_name
    


class ImportentReminders(models.Model):
    message = EncryptedTextField(help_text="Reminder message content")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the reminder was created")

    def __str__(self):
        return f"Reminder {self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class HelpAndSupport(models.Model):
    title = EncryptedCharField(max_length=500, help_text="Help topic title")
    content = EncryptedCharField(max_length=700, help_text="Frequently asked question")
    answer = EncryptedTextField(help_text="Answer to the question")

    def __str__(self):
        return self.content


class LotteryInfo(models.Model):
    title = EncryptedCharField(max_length=200)
    description = EncryptedTextField()

    def __str__(self):
        return self.title


class AccountSupport(models.Model):
    established = EncryptedCharField(max_length=200)
    draw_time = models.TimeField()
    draw_location = EncryptedCharField(max_length=255)
    ticket_price = EncryptedCharField(max_length=100)
    age_requirement = EncryptedCharField(max_length=100)
    claim_period = EncryptedCharField(max_length=100)

    def __str__(self):
        return f"Account Support"


class WeeklySchedule(models.Model):
    day = EncryptedCharField(max_length=600)
    lottery_name = EncryptedCharField(max_length=700)
    draw_time = models.TimeField()

    def __str__(self):
        return f"{self.day} - {self.lottery_name}"


class ImportantRule(models.Model):
    rule = EncryptedCharField(max_length=555)

    def __str__(self):
        return self.rule


class SafetyRule(models.Model):
    rule = EncryptedCharField(max_length=655)

    def __str__(self):
        return self.rule


class OfficialResource(models.Model):
    label = EncryptedCharField(max_length=1500)
    link = models.URLField()

    def __str__(self):
        
        
        
        return self.label    
# help and support    
class GeneralHelp(models.Model):
    title = EncryptedCharField(max_length=1300)
    description = EncryptedTextField()

    def __str__(self):
        return self.title
    
    
    
    
class accountsupporthelp(models.Model):
    title = EncryptedCharField(max_length=1300)
    description = EncryptedTextField()

    def __str__(self):
        return self.title    
    
    
    
class paymentandsubscriptionhelp(models.Model):
    title = EncryptedCharField(max_length=1300)
    description = EncryptedTextField()

    def __str__(self):
        return self.title    
        
        
        
class purchaselotteryhelp(models.Model):
    title = EncryptedCharField(max_length=1300)
    description = EncryptedTextField()

    def __str__(self):
        return self.title           
    
    
    
class ContactSupport(models.Model):
    support_email = models.EmailField()
    support_hours = EncryptedCharField(max_length=1200)
    closed_info = EncryptedCharField()

    def __str__(self):
        return self.support_email


class TermsAndConditions(models.Model):
    title = EncryptedCharField(max_length=500, help_text="Terms and Conditions title")
    content = EncryptedTextField(help_text="Terms and conditions content")
    created_at = models.DateTimeField(auto_now=True, help_text="Timestamp when created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when last updated")

    def __str__(self):
        return f"Terms and Conditions (Last updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')})"
    

class PrivacyPolicy(models.Model):
    title = EncryptedCharField(max_length=500, help_text="Privacy Policy title")
    content = EncryptedTextField(help_text="Privacy policy content")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when last updated")
    created_at = models.DateTimeField(auto_now=True, help_text="Timestamp when created")
    def __str__(self):
        return f"Privacy Policy (Last updated: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')})"  
    

