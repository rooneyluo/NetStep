from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from features.user.repository import UserRepository
from features.user.service import UserService
from features.user.schemas import UserCreate, UserResponse
from db.session import get_db

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        user = await user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
