from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from features.user.repository import UserRepository
from features.auth.service import AuthService
from db.session import get_db
from features.auth.schemas import SignupRequest, LoginRequest, TokenResponse
from features.user.exceptions import UserExistsError, UserCreateError
from features.user.schemas import UserResponse

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def sign_up(data: SignupRequest, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    try:
        user = await auth_service.sign_up(data)
        return user
    except UserCreateError as e:
        raise HTTPException(status_code=400, detail="Failed to create user")
    except UserExistsError as e:
        raise HTTPException(status_code=400, detail="User already exists")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    try:
        token = await auth_service.login_with_password(data)
        return token
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

"""
@router.post("/oauth/login", response_model=TokenResponse)
async def oauth_login(provider: str, token: str, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    try:
        jwt_token = await auth_service.login_with_oauth(provider, token)
        return jwt_token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
"""