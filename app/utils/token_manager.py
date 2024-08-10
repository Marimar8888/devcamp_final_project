import jwt
from app.config import Config
from datetime import datetime, timedelta

def decode_token(auth_header):
      
    if not auth_header:
         raise ValueError('Token is missing')
    
    try:
        token = auth_header.split(" ")[1]
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError('Token has expired')
    except jwt.InvalidTokenError as e:
        raise ValueError(f'Invalid Token: {str(e)}')
    except Exception as e:
        raise ValueError(f'Unexpected error: {str(e)}')

def encode_token(user_id):

    token_payload = {
        'users_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(token_payload, Config.SECRET_KEY, algorithm='HS256')

    return token