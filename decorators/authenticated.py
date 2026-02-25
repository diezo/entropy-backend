from fastapi import Request, HTTPException
from core import PostgresManager
from models import User
from api.v1.auth.service import decode_jwt_token

db = PostgresManager().session

def authenticated(req: Request):
    """
    FastAPI utility to authenticate endpoints.
    """
    
    auth_header = req.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    token = auth_header.split(" ")[1]
    
    try: payload = decode_jwt_token(token)
    except Exception: raise HTTPException(status_code=401, detail="Unauthorized")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user
