import os
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from api.v1.users import router as user_router
from api.v1.auth import router as auth_router
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
CORS_ALLOW_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:8080").split(",")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Serve frontend
#app.mount("/", StaticFiles(directory="/path/to/your/frontend/dist", html=True), name="static")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
