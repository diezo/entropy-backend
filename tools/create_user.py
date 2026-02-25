import sys
from pathlib import Path

# Add parent directory to path so we can import from core
sys.path.insert(0, str(Path(__file__).parent.parent))

from admin import AuthManager

auth: AuthManager = AuthManager()

# Ask for user details
username = input("Username: ")
can_upload_videos = input("Can upload videos? (y/N): ").lower() == "y"

# Create user
user = auth.new_user(
    username=username,
    can_upload_videos=can_upload_videos,
)

print(f"User ID: {user.user_id}")
print(f"Password: {user.password}")
