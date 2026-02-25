from dataclasses import dataclass


@dataclass
class PreSignedURL:
    """
    Represents a pre-signed URL for S3 uploads.
    """
    
    upload_url: dict
    object_key: str
