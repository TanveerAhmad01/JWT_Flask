import jwt
import datetime
import os
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")

def encode_auth_token(username):
    """
    Generates the JWT Auth Token
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=180),  
            'iat': datetime.datetime.utcnow(),  # Issued at
            'sub': username  # Subject (user identifier)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token):
    """
    Decodes the JWT Auth Token
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
