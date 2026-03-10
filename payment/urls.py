from django.urls import path
from payment.views import PaymentHistory, PaymentSession, StripeWebhook, payment_cancel, payment_success


urlpatterns = [
    path("payment/create-session/", PaymentSession.as_view(), name="create-payment-session"),
    path("payment/success/", payment_success, name="payment-success"), 
    path("payment/cancel/", payment_cancel  , name="payment-cancel"),
    path("stripe/webhook/", StripeWebhook.as_view(), name="stripe-webhook"),
    path("payment/history/", PaymentHistory.as_view(), name="payment-history"),
]