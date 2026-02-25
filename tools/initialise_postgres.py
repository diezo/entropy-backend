from sqlalchemy.orm import DeclarativeBase
import sys
from pathlib import Path

# Add parent directory to path so we can import from core
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.postgres_manager import PostgresManager

class Base(DeclarativeBase):
    pass


if __name__ == "__main__":
    
    # Proceed if 'yes' selected
    if input("Create initial tables? (y/N): ").lower() != "y":
        print("Aborting...")
        exit(0)
    
    engine = PostgresManager().engine
        
    if input("Drop existing tables? (y/N): ").lower() == "y":
        Base.metadata.drop_all(bind=engine)
        print("Existing tables dropped successfully!")

    # Import all models
    from models.video import *
    from models.user import *

    # Print all tables that will be created
    print("Tables to be created:")
    print(Base.metadata.tables)

    # Print engine url
    print(f"Engine URL: {engine.url}")

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("Tables created successfully!")
