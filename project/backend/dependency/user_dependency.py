from fastapi import HTTPException, Request
from database.db_utils import get_user_profile
from utils import verify_access_token
from model.user_model import UserResponse

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    current_user = get_user_profile(email=payload.get("sub"))

    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        role=current_user.role
    )