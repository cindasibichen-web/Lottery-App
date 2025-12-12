from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from lottery_app.models import *
from lottery_app.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from rest_framework import status
from lottery_web_app.serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




# subscription created successfully 
class SubscriptionPlanListCreateAPIView(APIView):
    """
    List all subscription plans or create a new plan (Admin only for create).
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all subscription plans",
        responses={200: SubscriptionPlanSerializer(many=True)}
    )
    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response({"message":"Subscription plan listed successfully",
                         "data" : serializer.data})

    @swagger_auto_schema(
        operation_description="Create a new subscription plan (Admin only)",
        request_body=SubscriptionPlanSerializer,
        responses={201: "Subscription Plan created successfully."}
    )
    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "Only admins can create plans."}, status=status.HTTP_403_FORBIDDEN)
        serializer = SubscriptionPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Subscription plan created successfully",
                             "data":serializer.data},status=status.HTTP_201_CREATED)
        return Response({"message":"Invalid data",
                         "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

# subscription plan edit delete api 
class SubscriptionPlanEditDeleteAPIView(APIView):
    """
    Retrieve, update, or delete a subscription plan (Admin only).
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return SubscriptionPlan.objects.get(pk=pk)
        except SubscriptionPlan.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a subscription plan by ID",
        responses={200: SubscriptionPlanSerializer()}
    )
    def get(self, request, pk):
        plan = self.get_object(pk)
        if not plan:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubscriptionPlanSerializer(plan)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a subscription plan (Admin only)",
        request_body=SubscriptionPlanSerializer,
        responses={200: "Subscription Plan updated successfully."}
    )
    def patch(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Only admins can update plans."}, status=status.HTTP_403_FORBIDDEN)
        plan = self.get_object(pk)
        if not plan:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubscriptionPlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Subscription plan updated successfully",
                             "data":serializer.data},status=status.HTTP_200_OK)
        return Response({"message":"Invalid data",
                         "errors" : serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a subscription plan (Admin only)",
        responses={204: "Subscription Plan deleted successfully."}
    )
    def delete(self, request, pk):
        if not request.user.is_staff:
            return Response({"detail": "Only admins can delete plans."}, status=status.HTTP_403_FORBIDDEN)
        plan = self.get_object(pk)
        if not plan:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        plan.delete()
        return Response({"message":"Subscription plan deleted successfully"},status=status.HTTP_204_NO_CONTENT)


