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
# Create your views here.

# create lottery 
class LotteryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Create a new lottery entry. Requires authentication.",
        request_body=LotterySerializer,
        responses={
            201: openapi.Response(description="Advertisement created successfully"),
            400: openapi.Response(description="Validation Error"),
            401: openapi.Response(description="Authentication credentials were not provided or invalid."),
        },
    )

    def post(self, request):
        serializer = LotterySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user.userprofile)
            return Response({
                "success": True,
                "message": "Lottery created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



# patch lottery 
class LottryPatchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            lottery = Lottery.objects.get(id=pk)
        except Lottery.DoesNotExist:
            return Response({"success": False, "message": "Lottery not found"}, status=404)

        serializer = LotterySerializer(lottery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True,
                             "message": "Lottery updated successfully",
                             "data": serializer.data})
        return Response({"success": False,
                         "message": "Invalid data",
                         "errors": serializer.errors}, status=400) 
    

# LOTTERY DELETE API VIEW
class LotteryDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, lottery_id):
        try:
            # Ensure the lottery belongs to the logged-in user
            lottery = Lottery.objects.get(id=lottery_id, created_by=request.user.userprofile)
        except Lottery.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Lottery not found or you don't have permission to delete it."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete the lottery
        lottery.delete()
        return Response(
            {
                "success": True,
                "message": "Lottery deleted successfully."
            },
            status=status.HTTP_200_OK
        )

