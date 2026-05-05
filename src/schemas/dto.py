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


class ExampleCreate(BaseModel):
    name: str


class ExampleRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
