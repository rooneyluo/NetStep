from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional

class LoginRequest(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_email_or_username(cls, values):
        if not values.email and not values.username:
            raise ValueError("Either email or username is required")
        return values
    
class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    token_type: str | None