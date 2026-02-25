import jwt
from datetime import datetime, timedelta

SECRET_KEY: str = "<jwt-secret-key>"
ALGORITHM: str = "HS256"


def generate_jwt_token(user_id: str) -> str:
    """
    Generates a JWT token for user authentication.
    """
    
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)  # Expires in 7 days
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_jwt_token(token: str) -> dict:
    """
    Decodes a JWT token and returns the payload.
    
    Raises: Exception if token is invalid or expired.
    """
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload