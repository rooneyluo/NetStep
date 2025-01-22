from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from features.user.repository import UserRepository
from features.user.service import UserService
from features.user.schemas import UserCreate, UserResponse, UserUpdate
from db.session import get_db
from features.user.exceptions import UserNotFoundError, UserExistsError, UserDeleteError, UserCreateError, UserUpdateError

router = APIRouter()

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        user = await user_service.create_user(user_data)
        return user
    except UserCreateError as e:
        raise HTTPException(status_code=400, detail="User create error")
    except UserExistsError as e:
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))            

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        users = await user_service.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{identifier}", response_model=UserResponse)
async def get_user(identifier: str, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        identifier = int(identifier) if identifier.isdigit() else identifier
        user = await user_service.get_user(identifier)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{identifier}", response_model=UserResponse)
async def update_user(identifier: str, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        identifier = int(identifier) if identifier.isdigit() else identifier
        user = await user_service.update_user(identifier, user_data)
        return user
    except UserUpdateError as e:
        raise HTTPException(status_code=400, detail="User update error")
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{identifier}")
async def delete_user(identifier: str, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        identifier = int(identifier) if identifier.isdigit() else identifier
        await user_service.delete_user(identifier)
        return {"message": "User deleted successfully"}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail="User not found")
    except UserDeleteError as e:
        raise HTTPException(status_code=400, detail="User delete error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))