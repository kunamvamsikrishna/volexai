from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from authentication.oauth import google_exchange_code , google_oauth_get_userinfo   
from .models import User
from rest_framework.response import Response
from authentication.seralizers import ApiKeySerializer, LoginSerializer, SignUpSerializer , ApikeyUpdateSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.utlis import generate_api_key 
from authentication.models import ApiKey


class Signup(APIView):
    permission_classes = []
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()
        if user:
             return Response({"message":"User with this email already exists"}, status=400)
        serializer = SignUpSerializer(data={"email":email,"password":password})
        if serializer.is_valid():
             user = serializer.save()
             data  =  user.sign_with_email_and_password(email,password)
             return Response({"message":"User created successfully","data":data}, status=201)
        
        # else:
        return Response(serializer.errors, status=400)
    


class Login(APIView):
     permission_classes = []
     def post(self,request):
            email = request.data.get("email")
            password = request.data.get("password")
            seralizer = LoginSerializer(data={"email":email,"password":password})
            if not seralizer.is_valid():
                    return Response(seralizer.errors, status=400)
            user = User.objects.filter(email=email).first()
            data  =  user.sign_with_email_and_password(email,password)
            return Response({"message":"User signed in successfully","data":data}, status=200)


class Userdetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
            seralizer = UserSerializer(request.user)
            return Response({"message":"User details fetched successfully","data":{"user":seralizer.data}}, status=200)


class Apikeys(APIView):
     permission_classes = [IsAuthenticated]
     def post(self,request):
          user = request.user
          name = request.data.get("name")
          if ApiKey.objects.filter(name=name,user=user).exists():
               return Response({"message":"API key with this name already exists"}, status=400)
          if not name:
               return Response({"message":"Name is required"}, status=400)
          raw_key, hashed_key = generate_api_key(user)     
          APIKEY = ApiKey.objects.create(user=user, name=name, key=hashed_key)
          return Response({"message":"API key created successfully","data":raw_key}, status=201)

     def get(self,request):
          user = request.user
          api_keys = ApiKey.objects.filter(user=user)
          serializer = ApiKeySerializer(api_keys, many=True)
          return Response({"message":"API keys fetched successfully","data":serializer.data}, status=200)


class refeshtoken(APIView):
     permission_classes = [AllowAny]
     def post(self,request):
           refresh_token = request.data.get("refresh_token")
           if not refresh_token:
                return Response({"message":"Refresh token is required"}, status=400)
           return User.objects.get_refresh_token(refresh_token)
     
     
class Apikeyid(APIView):
     permission_classes = [IsAuthenticated]
     def put(self,request,id):
          api_key = ApiKey.objects.filter(id=id,user=request.user).first()
          if not api_key:
               return Response({"message":"API key not found"}, status=404)
          serializer = ApikeyUpdateSerializer(data=request.data,context={"request":request},instance=api_key,partial=True,)
          if serializer.is_valid():
               serializer.save()
               return Response({"message":"API key updated successfully","data":serializer.data}, status=200)
          return Response(serializer.errors, status=400)
     


class GoogleAuth(APIView):
     permission_classes = [AllowAny]
     def get(self,request):
          code = request.GET.get("code")
          if not code:
               return Response({"message":"Code is required"}, status=400)
          try:
               access_token = google_exchange_code(code)
          except Exception as e:
               return Response({"message":"Something went wrong","error":str(e)}, status=500)
          try:
               user_info = google_oauth_get_userinfo(access_token)
          except Exception as e:         
               return Response({"message":"Something went wrong","error":str(e)}, status=500)
          email = user_info.get("email")
          if not email:
               return Response({"message":"Email not found in user info"}, status=400)
          try:
               user = User.objects.get(email=email)
               if user.auth_type!="google":
                    return Response({"message":"User with this email already exists with different auth type"}, status=400)
          except User.DoesNotExist:         
                user = User.objects.create_user_with_google_oauth(email=email)
          
          res = user.sign_with_oauth_google()
          return Response(res, status=200)