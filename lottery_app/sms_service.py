import random
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def generate_otp():
    """Generate a 6-digit OTP"""
    return random.randint(100000, 999999)


def send_otp_via_twilio(phone, otp):
    """
    Send OTP via Twilio SMS API
    phone: recipient phone number (must include country code, e.g., +919876543210)
    """
    try:
        # Initialize Twilio client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Prepare the message content
        message_body = f"Your OTP for password reset is {otp}. Please do not share it with anyone."

        # Send the SMS
        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,  # e.g. '+1234567890'
            to=phone
        )

        return {
            "success": True,
            "sid": message.sid,
            "status": message.status,
            "message": "OTP sent successfully."
        }

    except TwilioRestException as e:
        # Handle Twilio-specific errors gracefully
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to send OTP via Twilio."
        }

    except Exception as e:
        # Catch unexpected errors
        return {
            "success": False,
            "error": str(e),
            "message": "An unexpected error occurred while sending OTP."
        }
