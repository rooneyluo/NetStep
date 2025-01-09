from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# 基本用戶信息
class UserBase(BaseModel):
    email: EmailStr

# 用戶創建模型，包含密碼
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    role: Optional[str] = "user"

# 用戶登錄模型，只包含電子郵件和密碼
class UserLogin(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    role: Optional[str] = None

# 用戶更新模型，允許部分更新
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters long")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    photo: Optional[str] = None

# 用戶響應模型，不包含密碼
class UserResponse(BaseModel):
    username: str
    email: EmailStr
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    photo: Optional[str] = None
