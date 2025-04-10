from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=3, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=100)
    plan: Optional[str] = Field(None, regex='^(free|premium)$')

class UserInDB(UserBase):
    id: int
    reputacion: int
    plan: str
    verificado: bool
    fecha_registro: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str