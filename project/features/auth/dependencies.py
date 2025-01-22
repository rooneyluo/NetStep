from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token
from features.user.repository import UserRepository
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        user_repo = UserRepository(db)
        user = await user_repo.get_user_by_email(payload.get("email"))
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
