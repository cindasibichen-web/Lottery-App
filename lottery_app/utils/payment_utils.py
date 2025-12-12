# utils/stripe_utils.py
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(amount_cents, plan, user, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {"name": f"{plan.title} Plan"},
                    "unit_amount": amount_cents,
                },
                "quantity": 1,
            }
        ],
        metadata={
            "user_id": user.id,
            "plan_id": plan.id,
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
