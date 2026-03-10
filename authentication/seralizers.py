from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework import serializers
from authentication.models import ApiKey

class SignUpSerializer(serializers.ModelSerializer):
     
     class Meta:
          model = User
          fields = ['email','password']
     def create(self,validated_data):
          user = User.objects.create_user(
               email=validated_data['email'],
               password=validated_data['password']
          )
          return user
     
class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True, write_only=True)
        def validate(self,data):
            email = data.get("email")
            password = data.get("password")
            if not email or not password:
                raise serializers.ValidationError("Email and password are required")
            
            user = User.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError("User with this email does not exist")
            
            if user.auth_type != 'email':
                raise serializers.ValidationError(f"This user is registered with {user.auth_type}. Please use that method to login.")
            
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password")
            
          
            return data


class ApiKeySerializer(serializers.ModelSerializer):
     class Meta:
        model = ApiKey
        fields = ['id' ,'name', 'key', 'created_at', 'last_used_at' , 'is_active']
            
class ApikeyUpdateSerializer(serializers.ModelSerializer):
     class Meta:
        model = ApiKey
        fields = ['is_active' ,'name']
     def validate_name(self,value):
        user = self.context["request"].user
        existing = ApiKey.objects.filter(user=user, name=value)
        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise serializers.ValidationError(
                "You already have an API key with this name."
            )
        return value
     

class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id', 'email', 'auth_type', 'is_active', 'date_joined', 'last_login', 'is_staff', 'is_superuser' ,"is_verified"]