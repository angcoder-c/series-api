"""Servicio base con operaciones de alto nivel (esqueleto).

Implementa la lógica de aplicación (casos de uso) usando repositorios.
"""
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, repository):
        self.repo = repository

    # Métodos placeholder: implementar lógicamente según el caso de uso
    async def create(self, db, obj_in) -> T:
        return await self.repo.create(db, obj_in)

    async def get(self, db, id: int) -> T | None:
        return await self.repo.get(db, id)

    async def update(self, db, id: int, obj_in) -> T:
        return await self.repo.update(db, id, obj_in)

    async def delete(self, db, id: int) -> None:
        await self.repo.delete(db, id)
