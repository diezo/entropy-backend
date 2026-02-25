import os
from fastapi import APIRouter, Depends
from .schemas import UploadVideoRequest
from dotenv import load_dotenv
import random
from core.postgres_manager import PostgresManager
from models import User, Video
from decorators import authenticated
from core.s3_manager import S3Manager
from uuid import UUID
import string
from uuid import uuid4
from objects import PreSignedURL

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

DEBUG = os.getenv("DEBUG", "false") == "true"
router = APIRouter()

# Initialize helper classes
s3_manager = S3Manager(
    region_name="ap-south-1",
    debug=DEBUG
)

db = PostgresManager().session

@router.post("/upload")
def upload_video(
    current_user: User = Depends(authenticated),
    req: UploadVideoRequest = None
):
    """
    Uploads video details to Database and generates pre-signed URL for S3 upload.
    """
    
    # Permission check - can user upload videos?
    if not current_user.can_upload_videos:
        return {
            "status": "fail",
            "message": "You don't have permission to upload videos."
        }
    
    user_id: UUID = current_user.id
    
    # Parse video details
    filename: str = req.filename.strip()
    title: str = req.title.strip()
    description: str = req.description.strip()

    # Prepare video object    
    video_obj = Video(
        title=title,
        description=description,
        user_id=user_id
    )
    
    # Insert video object
    db.add(video_obj)
    db.commit()
    
    # Generate presigned url in S3
    url_object: PreSignedURL = s3_manager.generate_presigned_url(
        user_id=user_id,
        filename=filename,
        video_id=video_obj.id
    )

    return {
        "status": "ok",
        "upload_url": url_object.upload_url,
        "object_key": url_object.object_key
    }
