

from rest_framework import serializers
from payment.models import Payment


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id","stripe_id", "amount", "status", "created_at", "completed_at"]
