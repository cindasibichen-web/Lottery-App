from django.urls import path 
from lottery_web_app.views.lottery_views import *
from lottery_web_app.views.advertisment_views import *
from lottery_web_app.views.subscription_views import *

urlpatterns = [
    path('add-lottery/', LotteryCreateAPIView.as_view(), name='add-lottery'),
    
    path('lottery-update/<int:pk>/', LottryPatchAPIView.as_view(), name='lottery-update'),
    path('delete-lottery/<int:lottery_id>/', LotteryDeleteAPIView.as_view(), name='delete-lottery'),

    path('add-advertisement/', AdvertisementCreateAPIView.as_view(), name='add-advertisement'), 
    path('advertisement-update/<int:pk>/', AdvertisementUpdateAPIView.as_view(), name='advertisement-update'),
    
    path('delete-advertisement/<int:advertisement_id>/', AdvertisementDeleteAPIView.as_view(), name='delete-advertisement'),
    path('create-plans/', SubscriptionPlanListCreateAPIView.as_view(), name='plan-list-create'),
    path('subscription-plans/', SubscriptionPlanListCreateAPIView.as_view(), name='subscription-plans'),
    path('plan-edit-delete/<int:pk>/', SubscriptionPlanEditDeleteAPIView.as_view(), name='plan-edit-delete'),
   
]