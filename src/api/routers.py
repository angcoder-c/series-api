"""Routers esqueleto para exponer los endpoints CRUD.

Añadir rutas concretas usando FastAPI cuando se implemente la lógica.
"""
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/example", tags=["example"])


@router.get("/", summary="List examples")
async def list_examples():
    # TODO: implementar paginación y retorno con schemas
    return {"msg": "Listado de ejemplos (placeholder)"}


@router.post("/", summary="Create example")
async def create_example():
    # TODO: recibir schema, validar y delegar a servicio
    return {"msg": "Crear ejemplo (placeholder)"}

*** End Patch