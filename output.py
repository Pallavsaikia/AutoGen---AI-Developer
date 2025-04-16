import base64
import hashlib
import hmac
from datetime import datetime, timedelta

def base64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')

def create_jwt(user, secret):
    header = {
        'typ': 'JWT',
        'alg': 'HS256'
    }
    
    payload = {
        "username": user, 
        "exp": int((datetime.utcnow() + timedelta(days=30)).timestamp()),  
        "iat": int(datetime.utcnow().timestamp()),  # issued at time
    }
    
    encoded_header = base64url_encode(str.encode(json.dumps(header)))
    encoded_payload = base64url_encode(str.encode(json.dumps(payload)))
    
    signature = hmac.new(secret.encode(), msg=f"{encoded_header}.{encoded_payload}".encode(), digestmod=hashlib.sha256).digest()
    encoded_signature = base64url_encode(signature)
  
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"
    
user = 'username'  # replace with your username or user id
secret = 'YOUR_SECRET_KEY'  # replace with your secret key
jwt_string = create_jwt(user, secret)
print('The JWT string is:', jwt_string)