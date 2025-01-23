from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from features.user.repository import UserRepository
from features.auth.service import AuthService
from features.auth.schemas import SignupRequest, LoginRequest, TokenResponse
from features.user.exceptions import UserExistsError, UserCreateError
from features.user.schemas import UserResponse
from db.session import get_db
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

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
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    try:
        access_token, refresh_token = await auth_service.login_with_password(data)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token.token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=60 * 60 * 24 * 7,  # 7 days expiration
        )

        return access_token
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh-token", response_model=TokenResponse)
async def refresh_token(db: AsyncSession = Depends(get_db), refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    try:
        access_token = await auth_service.refresh_token(refresh_token)
        return access_token
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/oauth/login/{provider}", response_model=TokenResponse)
async def oauth_login(provider: str, code: str, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    try:
        access_token = await auth_service.login_with_oauth(provider, code)
        return access_token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/oauth/url")
async def oauth_url(provider: str):
    if provider == "google":
        return {"url": f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=profile email&access_type=offline&prompt=consent"}
    else:
        return {"url": "http://localhost"}
    