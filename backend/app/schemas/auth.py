from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    id: int
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class CreateUserRequest(BaseModel):

    username: str

    email: EmailStr