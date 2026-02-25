from core import PostgresManager
from models import User
from argon2 import PasswordHasher
from objects import UserCredentials
import secrets

PASSWORD_LENGTH_BYTES = 16


class AuthManager:
    """
    Manages user-related operations, including creation and authentication.
    """
    
    db = None
    ph = PasswordHasher()
    
    def __init__(self):
        """
        Initializes the UserManager with a PostgreSQL connection.
        """
        
        self.db = PostgresManager().session
    
    def new_user(self, username: str, can_upload_videos: bool = False) -> UserCredentials:
        """
        Creates a new user with randomized password.
        """
        
        # Generate secure random password
        password: str = secrets.token_hex(PASSWORD_LENGTH_BYTES)
        password_hash: str = self.ph.hash(password)
        
        # Prepare user object
        user_obj: User = User(
            username=username,
            password_hash=password_hash,
            display_name=username,
            can_upload_videos=can_upload_videos
        )
        
        # Save to database
        self.db.add(user_obj)
        self.db.commit()
        
        # Return user credentials
        return UserCredentials(
            user_id=user_obj.id,
            password=password
        )
