from fastapi import FastAPI
from dotenv import load_dotenv
from core.s3_manager import S3Manager
from api.v1 import videos, auth, server
import uvicorn
import os

load_dotenv()  # Load environment variables

DEBUG = os.getenv("DEBUG", "false") == "true"
app: FastAPI = FastAPI(debug=DEBUG)

# Include routers
app.include_router(videos.router, prefix="/api/v1/videos", tags=["Videos"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(server.router, prefix="/api/v1/server", tags=["Server"])

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=80,
        reload=DEBUG,
    )
