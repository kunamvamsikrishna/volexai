

from firebase_admin import auth
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import ApiKey, User
from firebase_admin._auth_utils import InvalidIdTokenError
import secrets
import hashlib
 

def get_token_from_header(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        return token
    except IndexError:
        return None
    
def decode_firebase_token(token):
        if not token:
         return None
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except InvalidIdTokenError:
            raise AuthenticationFailed("Invalid token")
        except Exception:
            raise AuthenticationFailed("Token verification failed")


def generate_api_key(user):
     prefix = f"volex-{user.email.split('@')[0]}-"
     raw_key = prefix + secrets.token_urlsafe(32)
     hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
     return  raw_key,hashed_key

def verify_api_key(raw_key):
     hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
     try:
        api_key_obj = ApiKey.objects.filter(key=hashed_key).first()
        if not api_key_obj:
                raise AuthenticationFailed("Invalid API key")
     except ApiKey.DoesNotExist:
        raise AuthenticationFailed("Invalid API key")
     if api_key_obj.is_active:
        return  api_key_obj