import boto3
from botocore.client import BaseClient
from objects import PreSignedURL
from uuid import UUID


class S3Manager:
    """
    Manages operations in AWS S3
    """
    
    RAW_UPLOADS_BUCKET = "entropy-raw-uploads-<env>"
    RAW_UPLOADS_EXPIRY = 600  # 10 minutes
    RAW_UPLOADS_MAX_SIZE = 500000000  # 500 MB
    
    s3: BaseClient
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """
        Ensures singleton behavior.
        """
        
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            
        return cls._instance
    
    def __init__(
        self,
        region_name: str,
        debug: bool
    ):
        """
        Initializes S3Manager with specified AWS region.
        
        :param region_name: AWS region name (e.g., "ap-south-1")
        """
        
        # Prevent re-initialization
        if self._initialized: return
        self._initialized = True
        
        # Setup bucket names based on environment
        self.RAW_UPLOADS_BUCKET = self.RAW_UPLOADS_BUCKET.replace("<env>", "dev" if debug else "prod")
        
        self.s3 = boto3.client("s3", region_name=region_name)

    def generate_presigned_url(
        self,
        user_id: UUID,
        filename: str,
        video_id: UUID
    ) -> PreSignedURL:
        """
        Generates pre-signed upload url for specified bucket.
        
        :param user_id: User ID
        :return: Pre-signed url
        :rtype: PreSignedURL
        """
        
        object_key: str = f"{str(user_id)}/{str(video_id)}/{filename}"
        
        # Generate upload url
        upload_url: dict = self.s3.generate_presigned_post(
            self.RAW_UPLOADS_BUCKET,
            object_key,
            Fields={
                "Content-Type": "video/mp4"
            },
            Conditions=[
                {"Content-Type": "video/mp4"},
                ["content-length-range", 0, self.RAW_UPLOADS_MAX_SIZE]
            ],
            ExpiresIn=self.RAW_UPLOADS_EXPIRY
        )
        
        return PreSignedURL(
            upload_url=upload_url,
            object_key=object_key
        )
