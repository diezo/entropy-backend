import os
from fastapi import APIRouter
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

DEBUG = os.getenv("DEBUG", "false") == "true"
router = APIRouter()

@router.get("/info")
def get_info():
    """
    Returns basic information about the server.
    """

    # TODO: Fetch from config file
    return {
        "status": "ok",
        "title": "Entropy Private Server",
        "description": "Just a test server"
    }
