import os
from fastapi import APIRouter
from .schemas import AjaxRequest
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from dotenv import load_dotenv
import random
from .service import generate_jwt_token
from core.postgres_manager import PostgresManager
from models import User
from core.s3_manager import S3Manager
import string
from argon2 import PasswordHasher
from uuid import uuid4
from objects import PreSignedURL

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

DEBUG = os.getenv("DEBUG", "false") == "true"
router = APIRouter()

SESSION_TOKEN_LENGTH = 32

db = PostgresManager().session
ph = PasswordHasher()

@router.post("/ajax")
def ajax(req: AjaxRequest):
    """
    Authenticates the user and returns a session token.
    """
    
    # Parse credentials
    username: str = req.username.strip()
    password: str = req.password.strip()

    # Authenticate user
    user: User = db.query(User).filter(User.username == username).first()
    
    # Check if user exists
    if not user:
        return {
            "status": "fail",
            "error": "This user doesn't exist"
        }
    
    # Validate password
    try: ph.verify(user.password_hash, password)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return {
            "status": "fail",
            "error": "The password you entered is incorrect"
        }

    # Generate JWT token
    jwt_token: str = generate_jwt_token(str(user.id))

    # Return JWT token
    return {
        "status": "ok",
        "user_id": str(user.id),
        "jwt_token": jwt_token
    }
