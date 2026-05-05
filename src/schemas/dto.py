"""Pydantic DTOs para la API.

Contiene esquemas para validación de entrada/salida.
"""
from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class SeriesCreate(BaseModel):
    title: str
    description: str | None = None


class SeriesUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class SeriesRead(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        orm_mode = True
