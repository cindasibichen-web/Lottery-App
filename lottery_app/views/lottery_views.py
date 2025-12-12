
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




# api health check view
def health_check(request):
    return JsonResponse({"status": "OK", "message": "API is healthy"})


# list all lotteries
class LotteryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = getattr(request, 'lang', 'en')
        lotteries = Lottery.objects.all()
        serializer = LotterySerializer(lotteries, many=True, context={'lang': lang})
        return Response({"success":True,
                         "message" : "Lottery listed successfully",
                         "data":serializer.data})
    
# user profile get api
class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            # Fetch the related user profile
            user_profile = UserProfile.objects.select_related('user').get(user=user)
            serializer = UserProfileSerializer(user_profile)
            
            return Response(
                {
                    "success": True,
                    "message": "Profile details fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK
            )

        except UserProfile.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "User profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )
        


# draw lottery results using the draw number 
class LotteryResultAPIView(APIView):
    @swagger_auto_schema(
        operation_description="List lottery results. Requires authentication.",
        manual_parameters=[
            openapi.Parameter(
                'draw_no',
                openapi.IN_QUERY,
                description="Draw number (e.g., KN-596)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'draw_name',
                openapi.IN_QUERY,
                description="Draw name (e.g., Karunya Plus)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Date of the draw (format: YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],     
        responses={
            200: openapi.Response(description="Results listed successfully"),
            400: openapi.Response(description="Validation Error"),
            401: openapi.Response(description="Authentication credentials were not provided or invalid."),
        },
    )

    def get(self, request):
        draw_no = request.query_params.get("draw_no")
        draw_name = request.query_params.get("draw_name")
        date = request.query_params.get("date")

        # ✅ Validate that date is provided
        if not date:
            return Response(
                {"success": False, "message": "Please provide a date (e.g., 2025-11-06)"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Ensure at least one of draw_no or draw_name is given
        if not draw_no and not draw_name:
            return Response(
                {
                    "success": False,
                    "message": "Please provide either draw_no (e.g., KN-596) or draw_name (e.g., Karunya Plus).",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ Fetch data from external API
        url = "https://indialotteryapi.com/wp-json/klr/v1/history?limit=100&offset=0"
        response = requests.get(url)

        if response.status_code != 200:
            return Response(
                {"success": False, "message": "Failed to fetch data from source API"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        json_data = response.json()
        data = json_data.get("items", [])

        # ✅ Normalize inputs for robust matching
        normalized_draw_no = (
            draw_no.replace("-", "").replace(" ", "").lower() if draw_no else None
        )
        normalized_draw_name = (
            draw_name.strip().lower() if draw_name else None
        )

        # ✅ Filter results by date first
        date_filtered = [item for item in data if item.get("draw_date") == date]

        if not date_filtered:
            return Response(
                {
                    "success": False,
                    "message": f"No results found for the given date {date}.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # ✅ Further filter by draw_no or draw_name (if provided)
        result = None

        for item in date_filtered:
            code = str(item.get("draw_code", "")).replace("-", "").replace(" ", "").lower()
            name = str(item.get("draw_name", "")).strip().lower()

            if normalized_draw_no and code == normalized_draw_no:
                result = item
                break
            elif normalized_draw_name and name == normalized_draw_name:
                result = item
                break

        # ✅ Handle not found
        if not result:
            return Response(
                {
                    "success": False,
                    "message": f"No results found for the given parameters (draw_no={draw_no}, draw_name={draw_name}, date={date}).",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        # ✅ Check if already saved
        if Result.objects.filter(
            lottery_name=result.get("draw_name"),
            result_date=date
        ).exists():
            return Response(
                {
                    "success": True,
                    "message": f"Result already exists for {result.get('draw_name')} ({date}).",
                    "result": result,
                },
                status=status.HTTP_200_OK,
            )

        # ✅ Create or get related models
        # lottery, _ = Lottery.objects.get_or_create(
        #     lottery_name=result.get("draw_name"),
        #     defaults={"draw_date": date, "status": "completed"},
        # )
        # ✅ Save to Result table
        Result.objects.create(
            # lottery=lottery,
            lottery_name=result.get("draw_name"),
            # prize=prize,
            winning_number=result.get("first_ticket") or result.get("first_prize_no", ""),
            prizes=result,  # Save full JSON data
            location=result.get("location") or "",
            result_date=result.get("draw_date"),
            # uploaded_by=getattr(request.user, "userprofile", None),
        )

        # ✅ Success response
        return Response(
            {
                "success": True,
                "message": f"Result found for draw on {date}",
                "result": result,
            },
            status=status.HTTP_200_OK,
        )
    


# lucky number create list view 
class LuckyNumberView(APIView):
    permission_classes = [IsAuthenticated]
    

    def get(self, request):
        """
        Fetch all lucky numbers of the logged-in user.
        """
        user_profile = request.user.userprofile
        lucky_numbers = UsersLuckyNumber.objects.filter(user=user_profile).order_by('-created_at')
        serializer = LuckyNumberSerializer(lucky_numbers, many=True)
        return Response({"message":"Data listed successfully","data":serializer.data}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Create a new lucky number entry. Requires authentication.",
        request_body=LuckyNumberSerializer,
    )

    def post(self, request):
        """
        Add a new lucky number for the logged-in user.
        """
        serializer = LuckyNumberSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # create() in serializer attaches the user automatically
            return Response({"success":True,"message":"Created successfully","date":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success":False,"message":"Invalid data", "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

# showing hours , minutes and seconds for next draw time

class NextDrawTime(APIView):

    def get(self, request):
        # Indian timezone
        ist = pytz.timezone("Asia/Kolkata")

        # Current IST datetime
        now_ist = datetime.now(ist)

        # Today's draw time (3:30 PM)
        today_draw = now_ist.replace(hour=15, minute=30, second=0, microsecond=0)

        # If current time has passed today's 3:30 PM → use tomorrow
        if now_ist >= today_draw:
            today_draw = today_draw + timedelta(days=1)

        # Calculate difference
        diff = today_draw - now_ist

        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60

        return Response({
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "next_draw_time": today_draw.strftime("%Y-%m-%d %H:%M:%S")
        }, status=status.HTTP_200_OK)