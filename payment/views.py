from django.utils import timezone
from rest_framework.generics import ListAPIView
from aiohttp import request
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import stripe
from payment.models import Payment, Wallet  
from rest_framework import status
from payment.seralizer import PaymentHistorySerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentSession(APIView):
    def post(self, request):
            amount = request.data.get("amount")
            if not amount or float(amount) <= 0:
                return Response({"error": "Amount is required and must be a positive number"}, status=400)
            try:
               wallet = Wallet.objects.get(user=request.user)
            except wallet.DoesNotExist:
              return Response({"error": "Wallet not found"}, status=404)
            payment = Payment.objects.create(user=request.user, amount=amount)
            try:
                 stripe_amount = int(amount*100)

                 session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="payment",

                    line_items=[
                        {
                            "price_data": {
                                "currency": "usd",
                                "product_data": {
                                    "name": "Wallet Top-up",
                                },
                                "unit_amount": stripe_amount,
                            },
                            "quantity": 1,
                        }
                    ],

                    metadata={
                        "payment_id": payment.id,
                        "user_id": request.user.id,
                    },

                        success_url="http://localhost:8000/payment/success",
                        cancel_url="http://localhost:8000/payment/cancel",
                     )

                # save stripe session id
                 payment.stripe_id = session.id
                 payment.save()

                 return Response({"sessionId": session.url}, status=200)
            except Exception as e:
                 payment.status = 'failed'
                 payment.save()
                 return Response({"error": str(e)})
            # Here you would integrate with your payment gateway to create a payment session
            
            


def payment_success(request):
    return HttpResponse("Payment successful")


def payment_cancel(request):
    return HttpResponse("Payment cancelled")

class StripeWebhook(APIView):
    permission_classes = []  # Allow unauthenticated requests for webhook
    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response({"error": "Invalid signature"}, status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            payment_id = session["metadata"]["payment_id"]
            user_id = session["metadata"]["user_id"]

            try:
                payment = Payment.objects.get(id=payment_id, user_id=user_id)
                if payment.status == "completed":
                    return Response({"message": "Already processed"})
                payment.status = "completed"
                payment.completed_at = timezone.now()
                payment.save()

                wallet, created = Wallet.objects.get_or_create(user_id=user_id)
                wallet.credits += payment.amount
                wallet.save()
            except Payment.DoesNotExist:
                return Response({"error": "Payment not found"}, status=404)

        return Response({"message": "Webhook received"}, status=200)
    



class PaymentHistory(ListAPIView):
    serializer_class = PaymentHistorySerializer
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by("-created_at")
