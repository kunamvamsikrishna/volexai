
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import User, ApiKey
from authentication.utlis import decode_firebase_token, get_token_from_header, verify_api_key

class FirebaseAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = get_token_from_header(request)  

        if not token:
            return None  # No token = let DRF handle

        decoded_token = decode_firebase_token(token)

        if not decoded_token:
            raise AuthenticationFailed("Invalid jwt token")

        uid = decoded_token.get("uid")

        if not uid:
            raise AuthenticationFailed("Invalid token payload")

        user = User.objects.filter(firebase_uid=uid).first()

        if not user:
            raise AuthenticationFailed("User not found","here")

        return (user, None)
    


class APIkeyAuthentication(BaseAuthentication):

    def authenticate(self, request):
    
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No token
        api_key = auth_header.split(' ')[1]
     
        api_key_obj = verify_api_key(api_key)
        user = api_key_obj.user
        return (user, api_key_obj)