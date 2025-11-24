from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(["POST"])
def create_checkout_session(request):
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "ron",
                        "product_data": {
                            "name": "T-Shirt",
                            "images": ["https://static.vecteezy.com/system/resources/thumbnails/057/068/323/small/single-fresh-red-strawberry-on-table-green-background-food-fruit-sweet-macro-juicy-plant-image-photo.jpg", "https://static.vecteezy.com/system/resources/thumbnails/057/068/323/small/single-fresh-red-strawberry-on-table-green-background-food-fruit-sweet-macro-juicy-plant-image-photo.jpg"],
                            "metadata": {
                                "size": "L",
                                "color": "red",
                                "sku": "TSHIRT123"
                            },
                        },

                        "unit_amount": 2000,
                    },
                    "quantity": 2,
                },
                {
                    "price_data": {
                        "currency": "ron",
                        "product_data": {
                            "name": "Hat",
                            "images": ["https://example.com/hat.png"]
                        },
                        "unit_amount": 1500,
                    },
                    "quantity": 1,
                }
            ],
            success_url=request.build_absolute_uri("/payments/success/") + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri("/payments/cancel/"),
        )
        return Response({"url": session.url})
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return Response(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        print("Payment succeeded:", session["id"])

    if event["type"] == "payment_intent.payment_failed":
        pass

    return Response(status=200)
