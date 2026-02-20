from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserResponse(BaseModel):
    """
    Response model for user profile information.
    """
    name: str = Field(..., description="Full name of the user", example="John Doe")
    email: str = Field(..., description="Email address of the user", example="john@example.com")
    avatar_url: Optional[str] = Field(None, description="URL to the user's avatar image", example="https://lh3.googleusercontent.com/...")

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Response model for JWT access token.
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type, usually 'bearer'")

class Message(BaseModel):
    """
    Generic message response.
    """
    message: str = Field(..., description="Informational message", example="Operation successful")

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
