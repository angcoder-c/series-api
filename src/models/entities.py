"""ORM entity examples and placeholders.

Define your domain entities here as SQLAlchemy declarative models.
"""
from sqlalchemy import Column, Integer, String
from src.db import Base


class ExampleEntity(Base):
    """Ejemplo de entidad.

    Reemplaza o añade entidades reales según el dominio.
    """
    __tablename__ = "example"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
