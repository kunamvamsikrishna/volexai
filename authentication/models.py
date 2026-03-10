from random import choices
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import  AbstractUser
from .managers import UserManger
from rest_framework import status
from firebase_admin import auth
from django.utils import timezone
# Create your models here.
import requests
import json

class User(AbstractUser):
    AUTH_TYPES = (
        ('email', 'Email'),
        ('google', 'Google'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firebase_uid = models.CharField(max_length=255, unique=True,null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150,null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPES, default='email')  # e.g., 'email', 'google', 'facebook'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManger    ()

    def __str__(self):
        return self.username
    
    def sign_with_email_and_password(self,email,password):
        try:
            url = url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.FIREBASE_API_KEY}"
            headers = {"content-type": "application/json; charset=UTF-8"}
            body = {"email": email, "password": password, "returnSecureToken": True}
            response = requests.post(url, headers=headers, json=body)
            self.last_login = timezone.now()
            self.save()
            return response.json()
        except Exception as e:
            return e
    def sign_with_oauth_google(self):
            custom_token = auth.create_custom_token(self.firebase_uid)
            custom_token = custom_token.decode("utf-8")
            request_ref = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={0}".format(
                settings.FIREBASE_API_KEY
            )
            headers = {"content-type": "application/json; charset=UTF-8"}
            data = json.dumps({"token": custom_token, "returnSecureToken": True})
            request_object = requests.post(request_ref, headers=headers, data=data)
            self.last_login = timezone.now()
            self.save()
            return request_object.json()



class ApiKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="api_key")
    created_at = models.DateTimeField(auto_now_add=True)
    name  = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        unique_together = ('user', 'name')