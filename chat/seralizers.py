from .models import *
from rest_framework import serializers

class ChatsSerializer(serializers.ModelSerializer):
    model = serializers.SerializerMethodField(read_only=True)
    provider = serializers.CharField(read_only=True)
    class Meta:
        model = ChatSession
        fields = '__all__'
    def get_model(self, obj):
        return obj.model.name
    def get_provider(self, obj):
        return obj.model.provider.name
    


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = 'id', 'role', 'content', 'created_at', 'token_count'



class RequestSerializer(serializers.ModelSerializer):
    model = serializers.CharField(source='model.name', read_only=True)
    provider = serializers.CharField(source='model.provider.name', read_only=True)
    class Meta:
        model = Request
        fields = 'id','input_tokens', 'output_tokens', 'total_cost', 'status', 'request_type', 'created_at' ,'model'  ,'provider'