"""Model definitions for ORM entities using dataclasses.

Estos modelos representan la estructura de datos del dominio.
Usa dataclasses para mantener simplicidad (sin ORM).
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ExampleEntity:
    """Ejemplo de entidad de dominio.

    Reemplaza o añade entidades reales según el dominio.
    """
    id: Optional[int] = None
    name: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
