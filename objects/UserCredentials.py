from dataclasses import dataclass


@dataclass
class UserCredentials:
    """
    Stores user credentials for authentication.
    """
    
    user_id: str
    password: str
