from django.urls import path
from authentication import views


urlpatterns = [
    path('signup/',views.Signup.as_view(),name="signup"),
    path('login/',views.Login.as_view(),name="login"),
    path('userdetails/',views.Userdetails.as_view(),name="userdetails"),
    path('api-keys/',views.Apikeys.as_view(),name="api-keys"),
    path('api-key/<int:id>/',views.Apikeyid.as_view(),name="api-key-id"),
    path('refresh-token/',views.refeshtoken.as_view(),name="refresh-token"),            
    path('google/callback/',views.GoogleAuth.as_view(),name="google-callback"),
]