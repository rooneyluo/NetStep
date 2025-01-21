from fastapi import HTTPException, Request, status
from database.db_utils import get_user_profile
from utils.user_utils import verify_access_token
from model.user_model import UserResponse

async def get_current_user(request: Request) -> UserResponse:
    access_token = await get_bearer_token(request)

    if not access_token:
        raise HTTPException(status_code=401, detail="Access token missing")
    
    payload = verify_access_token(access_token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    current_user = get_user_profile(email=payload.get("sub"))

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        role=current_user.role
    )

async def get_bearer_token(request: Request) -> str:
    # Get the Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token missing or invalid",
        )
    # Extract the token from the "Bearer " prefix
    return auth_header[len("Bearer "):]