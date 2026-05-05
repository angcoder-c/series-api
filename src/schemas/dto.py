"""Pydantic DTOs para la API.

Contiene esquemas para creación y lectura de `ExampleEntity`.
"""
from pydantic import BaseModel


class ExampleCreate(BaseModel):
    name: str


class ExampleRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
