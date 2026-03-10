import requests
from django.conf import settings

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI
GOOGLE_OAUTH_TOKEN_URL = settings.GOOGLE_OAUTH_TOKEN_URL
GOOGLE_USER_INFO_URL = getattr(settings, 'GOOGLE_USER_INFO_URL', 'https://www.googleapis.com/oauth2/v2/userinfo')

def google_exchange_code(code):

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(
        GOOGLE_OAUTH_TOKEN_URL,
        data=data
    )

    response_data = response.json()

    return response_data["access_token"]


def google_oauth_get_userinfo(access_token):

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        GOOGLE_USER_INFO_URL,
        headers=headers
    )

    return response.json()