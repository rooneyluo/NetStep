from fastapi import HTTPException, Request
from database.db_utils import get_user_profile
from utils import verify_access_token
from model.user_model import UserUpdate

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    update_user = get_user_profile(email=payload.get("sub"))

    if not update_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return UserUpdate(
        username=update_user.username,
        email=update_user.email,
        first_name=update_user.first_name,
        last_name=update_user.last_name,
        phone_number=update_user.phone_number,
        photo=update_user.photo
    )