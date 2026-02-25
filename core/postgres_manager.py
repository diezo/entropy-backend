from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Load environment variables
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class PostgresManager:
    """
    Manages interactions with PostgreSQL database.
    """
    
    engine = None
    session = None
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """
        Ensures singleton behavior.
        """
        
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance
    
    def __init__(self):
        """
        Initializes PostgreSQL connection.
        """
        
        # Prevent re-initialization
        if self._initialized: return
        self._initialized = True
        
        # Create engine
        self.engine = create_engine(
            os.getenv("POSTGRESQL_URL"),
            echo=False
        )
        
        # Create session
        self.session = sessionmaker(bind=self.engine)()
