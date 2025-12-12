from django.urls import path 
from lottery_app.views.lottery_views import *
from lottery_app.views.advertisment_views import *
from lottery_app.views.cart_views import *
from lottery_app.views.basic_rules_sections import *
# from lottery_app views import *

urlpatterns = [


   path('health-check/', health_check, name='health-check'), 
   path('lotteries-list/', LotteryListAPIView.as_view(), name='lottery-list'),
   path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
   path('advertisment-list/', ActiveAdvertisementListView.as_view(), name='advertisment-list'),
   path("lottery-result/", LotteryResultAPIView.as_view(), name="lottery-result"),

   path('lucky-number-add-list/', LuckyNumberView.as_view(), name='lucky-number-add-list'),
   path("next-draw/", NextDrawTime.as_view(), name="next-draw"),

   path("cart/add/", AddToCartView.as_view()),
    path("cart-view/", UserCartAPI.as_view(), name="user-cart"),
    
    path("cartitemdelete/<int:pk>/", CartItemDeleteAPIView.as_view(), name="cart-item-delete"),
    
    path("cart-item-update-qty/<int:pk>/", CartItemUpdateQtyAPIView.as_view(), name="cart-item-update-qty"),
    path("price-claim-rules/", BasicRulesSectionsView.as_view(), name="price-claim-rules"),
    path("price-claim-rules/<int:pk>/", BasicRulesSectionEditDeleteAPIView.as_view(), name="price-claim-rules-edit-delete"),

    path("documents-required-add-list/", DocumentsRequiredPriceClaimView.as_view(), name="documents-required-add-list"),
    path("documents-required-edit-delete/<int:pk>/", DocumentsRequiredPriceClaimEditDeleteAPIView.as_view(), name="documents-required-edit-delete"),

    path("importent-reminders-add-list/", ImportentRemindersView.as_view(), name="importent-reminders-add-list"),
    path("importent-reminders-edit-delete/<int:pk>/", EditDeleteImportentRemindersAPIView.as_view(), name="importent-reminders-edit-delete"),
    # terms and conditions add and list api

    path("lottery-info-view/", LotteryInfoList.as_view(), name="lottery-info-view"),
   path("account-support-view/", AccountSupportList.as_view(), name="account-support-view"),
   path("weekly-schedule-view/", Weekly_Schedule_List.as_view(), name="weekly-schedule-view"),
   path("ImportantRule_List/", ImportantRule_List.as_view(), name="ImportantRule_List"),
    path("SaftyRule-List/", SaftyRule_List.as_view(), name="SaftyRule-List"),
    path("official-Resource-List/", OfficialResource_List.as_view(), name="official-Resource-List"),
    path("lottery-info-add/", LotteryInfoAdd.as_view(), name="lottery-info-add"),
    path("lottery-info-edit/<int:pk>/", LotteryInfoEdit.as_view(), name="lottery-info-edit"),
    path("lottery-info-delete/<int:pk>/", LotteryInfoDelete.as_view(), name="lottery-info-delete"),
    path("account-support-add/", AccountSupportAdd.as_view(), name="account-support-add"),
      path("account-support-edit/<int:pk>/", AccountSupportEdit.as_view(), name="account-support-edit"),
    path("account-support-delete/<int:pk>/", AccountSupportDelete.as_view(), name="account-support-delete"),
     path("add_Weekly_Schedule/", add_Weekly_Schedule.as_view(), name="add_Weekly_Schedule"),

      path("Weekly-Schedule-Edit/<int:pk>/", Weekly_ScheduleEdit.as_view(), name="Weekly-Schedule-Edit"),
      path("Weekly-Schedule-Delete/<int:pk>/", Weekly_ScheduleDelete.as_view(), name="Weekly-Schedule-Delete"),
      
      path("add_ImportantRule/", add_ImportantRule.as_view(), name="add_ImportantRule"),
      
      path("importantRule-Edit/<int:pk>/", ImportantRuleEdit.as_view(), name="ImportantRule-Edit"),
       path("importantRule-Delete/<int:pk>/", ImportantRuleDelete.as_view(), name="importantRule-Delete"),
       
       
       
    path("add-SafetyRule/", add_SafetyRule.as_view(), name="add-SafetyRule"),
    
       
    path("SafetyRule-Edit/<int:pk>/", SafetyRuleEdit.as_view(), name="SafetyRule-Edit"),
    path("SafetyRule-Delte/<int:pk>/", SafetyRuleDelete.as_view(), name="SafetyRule-Delte"),
    
     path("official-resource-add/", OfficialResourceAdd.as_view(), name="official-resource-add"),
    path("official-resource-edit/<int:pk>/", OfficialResourceEdit.as_view(), name="official-resource-edit"),
    path("official-resource-delete/<int:pk>/", OfficialResourceDelete.as_view(), name="official-resource-delete"),
  
  
    path("general-help-createview/", GeneralHelpListCreate.as_view(),name="general-help-createview"),
    path("general-help-editdelete/<int:pk>/", GeneralHelpEditDelete.as_view(),name="general-help-editdelete"),
       
    path("accountsupport-help-createview/", AccountsupporthelpListCreate.as_view(),name="general-help-createview"),
         
    path("account-support-helpEditDelete/<int:pk>/", AccountsupporthelpEditDelete.as_view(),name="account-support-helpEditDelete"),
           
           
          
    # List + Create
    path("payment-subscription-help-create/",paymentandsubscriptionhelpListCreate.as_view(), name="payment-subscription-help-create"),
    path("payment-subscription-help-editdelete/<int:pk>/",paymentandsubscriptionhelpEditDelete.as_view(), name="payment-subscription-help-editdelete"),
    
     path("purchase-lottery-help-createview/", PurchaseLotteryHelpListCreate.as_view(), name="purchase-lottery-help-createview"),
     path("purchase-lottery-help-editdelete/<int:pk>/", PurchaseLotteryHelpEditDelete.as_view(), name="purchase-lottery-help-editdelete"),
     
      path("contact-support-createview/", ContactSupportListCreate.as_view(),name="contact-support-createview"),
    path("contact-support-editdelete/<int:pk>/", ContactSupportEditDelete.as_view(),name="contact-support-editdelete"),
    path('terms-and-conditions/', TermsAndConditionAddListAPIView.as_view(), name='terms-and-conditions'),
    path('terms-and-conditions-edit-delete/<int:pk>/', TermsAndConditionsEditDeleteAPIView.as_view(), name='terms-and-conditions-edit-delete'),


    path("privacy-policy-add-list/", PrivacyPolicyAddListAPIView.as_view(), name="privacy-policy-add-list"),
    path("privacy-policy-edit-delete/<int:pk>/", PrivacyPolicyEditDeleteAPIView.as_view(), name="privacy-policy-edit-delete"),




]