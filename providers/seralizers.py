


from rest_framework import serializers
from .models import LLms , Providers


class LLmSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLms
        fields = "__all__"


class ProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providers
        fields = "__all__"