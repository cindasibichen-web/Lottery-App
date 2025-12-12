
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
from rest_framework import generics
from lottery_app.utils.transit_encryption import  *
from lottery_app.middleware.encryption_middleware import *


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.data) 
        decrypted_data = decrypt_request_payload(request)

        if decrypted_data:
            print(decrypted_data)
            # Replace request.data with decrypted version
            data = decrypted_data
        else:
            print(request.data)
            data = request.data
        lottery_id = data.get("lottery_id")

        if not lottery_id:
            response =  Response({
                "success": False,
                "message": "lottery_id is required."
            }, status=400)
            response.encrypt_payload = True
            return response


        try:
            lottery = Lottery.objects.get(id=lottery_id)
        except Lottery.DoesNotExist:
            response =  Response({
                "success": False,
                "message": "Lottery not found."
            }, status=404)
            response.encrypt_payload = True
            return response


        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if this lottery already exists in cart
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            lottery=lottery,
          #  defaults={"price": 40}  # Fix price as ₹40
        )

        if not created:
            item.quantity += 1
            item.save()

        response = Response({
            "success": True,
            "message": "Lottery added to cart successfully."
        })
        response.encrypt_payload = True
        return response
        
        
        
class UserCartAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        serializer = CartSerializer(cart)
        response =  Response({
            "success": True,
            "cart": serializer.data
        }, status=200)
        response.encrypt_payload = True
        return response
        
        
        
class CartItemDeleteAPIView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Allow deleting only items of the logged-in user
        return CartItem.objects.filter(cart__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                "success": True,
                "message": "Cart item deleted successfully"
            },
            status=status.HTTP_200_OK  # return 200 instead of 204
        )




class CartItemUpdateQtyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        action = request.data.get("action")

        try:
            cart_item = CartItem.objects.get(id=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"success": False, "message": "Item not found"}, status=404)

        # Update Quantity
        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease":
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                return Response({"success": False, "message": "Minimum quantity is 1"}, status=400)
        else:
            return Response({"success": False, "message": "Invalid action"}, status=400)

        cart_item.save()

        # Return Updated Cart with Grand Total
        cart = cart_item.cart
        serializer = CartSerializer(cart)

        return Response({
            "success": True,
            "cart": serializer.data
        }, status=200)


