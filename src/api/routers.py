"""Routers esqueleto para exponer los endpoints CRUD.

Añadir rutas concretas usando FastAPI cuando se implemente la lógica.
Usar conexiones psycopg2 via get_connection() y return_connection().
"""
from fastapi import APIRouter

router = APIRouter(prefix="/example", tags=["example"])


@router.get("/", summary="List examples")
async def list_examples(skip: int = 0, limit: int = 10):
    # TODO: implementar paginación y retorno con schemas
    # from src.db import get_connection, return_connection
    # conn = get_connection()
    # try:
    #     # usar conn.cursor() para ejecutar queries
    # finally:
    #     return_connection(conn)
    return {"msg": "Listado de ejemplos (placeholder)", "skip": skip, "limit": limit}


@router.post("/", summary="Create example")
async def create_example(data: dict):
    # TODO: recibir schema, validar y delegar a servicio
    # from src.db import get_connection, return_connection
    # conn = get_connection()
    # try:
    #     # usar conn.cursor() para insertar
    # finally:
    #     return_connection(conn)
    return {"msg": "Crear ejemplo (placeholder)", "data": data}