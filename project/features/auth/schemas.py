from pydantic import BaseModel, EmailStr, field_validator, ValidationInfo
from typing import Optional

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @field_validator('email', 'username')
    def check_email_or_username(cls, v, info: ValidationInfo):
        if not info.data.get('email') and not info.data.get('username'):
            raise ValueError("Either email or username is required")
        return v

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

