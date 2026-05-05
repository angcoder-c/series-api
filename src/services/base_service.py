"""Servicio base con operaciones de alto nivel (esqueleto).

Implementa la lógica de aplicación (casos de uso) usando repositorios y psycopg2.
"""
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class BaseService(Generic[T]):
    """Servicio genérico para operaciones CRUD."""

    def __init__(self, repository):
        self.repo = repository

    # Métodos placeholder: implementar lógicamente según el caso de uso
    async def create(self, conn, obj_in: dict) -> dict:
        """Crear un nuevo registro via repositorio."""
        return await self.repo.create(conn, obj_in)

    async def get(self, conn, id: int) -> Optional[dict]:
        """Obtener un registro por ID."""
        return await self.repo.get(conn, id)

    async def get_all(self, conn, skip: int = 0, limit: int = 10) -> List[dict]:
        """Obtener todos los registros."""
        return await self.repo.get_all(conn, skip, limit)

    async def update(self, conn, id: int, obj_in: dict) -> Optional[dict]:
        """Actualizar un registro."""
        return await self.repo.update(conn, id, obj_in)

    async def delete(self, conn, id: int) -> bool:
        """Eliminar un registro."""
        return await self.repo.delete(conn, id)
