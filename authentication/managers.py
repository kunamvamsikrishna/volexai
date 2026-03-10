
from django.db import models
from django.contrib.auth.models import BaseUserManager
from core import settings                                               
import requests
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth

class UserManger(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        try :
            response = self.create_with_email_and_password(email, password)
            uid  = response.get("localId")
            user = self.model(email=email, firebase_uid=uid,username=email.split("@")[0])
            user.set_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            return e

    def create_with_email_and_password(self, email, password):
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={settings.FIREBASE_API_KEY}"
            headers = {"content-type": "application/json; charset=UTF-8"}
            body = {"email": email, "password": password, "returnSecureToken": True}
            reponse = requests.post(url, headers=headers, json=body)
            return reponse.json()
        except Exception as e:
            return e
    def get_refresh_token(self, refresh_token):
        try:
            url = f"https://securetoken.googleapis.com/v1/token"
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
            params = {
                "key": settings.FIREBASE_API_KEY
            }
            response = requests.post(url, params=params, data=payload)
            data = response.json()

            if "error" in data:
                return Response(
                    {"error": "Invalid refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            return Response({
                "id_token": data["id_token"],
                "expires_in": data["expires_in"],
                "refresh_token": data["refresh_token"]
            })
        except Exception as e:
          
            return e
    def create_user_with_google_oauth(self,email):
        try:
            firebaseuser = auth.create_user(email=email)
            user = self.model(email=email,firebase_uid=firebaseuser.uid,username=email.split("@")[0],auth_type="google")
            user.set_unusable_password()
            user.save(using=self._db)
            return user
        except Exception as e:
             raise(e)