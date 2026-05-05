"""Base repository interface para operaciones CRUD con psycopg2.

Implementa adaptadores concretos heredando de esta clase.
"""
from typing import List, Optional, Any
from abc import ABC, abstractmethod
import psycopg2.extras


class BaseRepository(ABC):
    """Interfaz base para repositorios (CRUD con psycopg2)."""

    @abstractmethod
    async def create(self, conn, obj_in: dict) -> dict:
        """Crear un nuevo registro."""
        pass

    @abstractmethod
    async def get(self, conn, id: int) -> Optional[dict]:
        """Obtener un registro por ID."""
        pass

    @abstractmethod
    async def get_all(self, conn, skip: int = 0, limit: int = 10) -> List[dict]:
        """Obtener todos los registros con paginación."""
        pass

    @abstractmethod
    async def update(self, conn, id: int, obj_in: dict) -> Optional[dict]:
        """Actualizar un registro."""
        pass

    @abstractmethod
    async def delete(self, conn, id: int) -> bool:
        """Eliminar un registro."""
        pass
