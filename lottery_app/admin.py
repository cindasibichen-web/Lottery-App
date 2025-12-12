from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(DealerProfile)
admin.site.register(Lottery)
admin.site.register(Prize)
admin.site.register(Result)
admin.site.register(Prediction)
admin.site.register(Subscription)
admin.site.register(SubscriptionPlan)
admin.site.register(Payment)
admin.site.register(Advertisement)
admin.site.register(UsersLuckyNumber)
admin.site.register(Notification)
admin.site.register(PriceClaimRule)
admin.site.register(DocumentsRequiredForPrizeClaim)
admin.site.register(ImportentReminders)
admin.site.register(HelpAndSupport)
admin.site.register(TermsAndConditions)
admin.site.register(PrivacyPolicy)