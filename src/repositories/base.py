"""Interfaces y contratos para repositorios (CRUD).

Usa estos protocolos/abstracciones para implementar adaptadores concretos.
"""
from typing import Generic, TypeVar, Protocol, Optional
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class Repository(Protocol, Generic[T]):
    async def create(self, db: AsyncSession, obj_in) -> T: ...

    async def get(self, db: AsyncSession, id: int) -> Optional[T]: ...

    async def update(self, db: AsyncSession, id: int, obj_in) -> T: ...

    async def delete(self, db: AsyncSession, id: int) -> None: ...
