from fastapi import APIRouter, HTTPException, Response, Request, Depends
from database.db_utils import get_user_for_authentication, add_user, update_user_info, get_user_profile
from model.user_model import UserResponse, UserCreate, UserLogin, UserUpdate
from utils.user_utils import verify_password, hash_password, verify_access_token, verify_refresh_token, create_access_token, create_refresh_token
from dependency.user_dependency import get_current_user, get_bearer_token
from utils.utils import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/register")
async def register(user: UserCreate):
    existing_user = get_user_profile(email=user.email)
    if existing_user:
        logger.warning(f"User with email {user.email} already exists")
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash the password and try to add the user to the database
    try:
        new_user = add_user(username=user.email, email=user.email, password=hash_password(user.password), role="user")
    except Exception as e:
        logger.error(f"Error adding user to the database: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

    # If the user already exists, return a 400 error
    if new_user is None:
        logger.warning(f"Failed to create user for email {user.email}")
        raise HTTPException(status_code=400, detail="Failed to create user")
    
    logger.info(f"User {new_user.username} registered successfully")

    return {"user": UserResponse(username=new_user.username, email=new_user.email, role=new_user.role)}

@router.post("/login")
async def login(user: UserLogin, response: Response):
    if user.email is None and user.username is None and user.phone_number is None:
        raise HTTPException(status_code=400, detail="Email, username or phone number is required")
    
    # Fetch user from the database by email
    db_user = get_user_for_authentication(user.username, user.email, user.phone_number)
    
    # Check if user exists and verify the password
    if db_user is None or not verify_password(user.password, db_user.password):
        logger.warning(f"Failed login attempt for user {user.email}")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="strict")

    logger.info(f"User {db_user.username} logged in successfully")

    return {"access_token": access_token, "user": UserResponse(username=db_user.username, email=db_user.email, role=db_user.role)}

@router.get("/verify-token")
async def verify_token(access_token: str = Depends(get_bearer_token)):
    payload = verify_access_token(access_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid access token")

    db_user = get_user_for_authentication(email=payload.get("sub"))

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    return {"user": UserResponse(username=db_user.username, email=db_user.email, role=db_user.role)}

@router.get("/refresh-token")
async def refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    payload = verify_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(data={"sub": payload.get("sub")})

    return {"access_token": access_token}

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    logger.info("User logged out successfully")
    return {"message": "Logged out successfully"}

@router.post("/update_user")
async def update_user(user_update: UserUpdate, current_user: UserResponse = Depends(get_current_user)):
    # 更新用戶資料
    try:
        updated_user = update_user_info(current_user, user_update)
    except Exception as e:
        logger.error(f"Error updating user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

    if not updated_user:
        raise HTTPException(status_code=400, detail="Failed to update user")

    return {"user": UserResponse(username=updated_user.username, email=updated_user.email, role=updated_user.role, first_name=updated_user.first_name, last_name=updated_user.last_name, phone_number=updated_user.phone_number, photo=updated_user.photo)}

