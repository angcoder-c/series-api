"""Endpoints para Géneros."""
from fastapi import APIRouter, HTTPException, Depends
from src.db import get_connection, return_connection
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("")
async def list_genres(skip: int = 0, limit: int = 100):
    """Get all genres"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name FROM genres ORDER BY name LIMIT %s OFFSET %s",
                (limit, skip)
            )
            return [
                {"id": row[0], "name": row[1]}
                for row in cur.fetchall()
            ]
    finally:
        return_connection(conn)


@router.post("")
async def create_genre(genre: dict, current_user: dict = Depends(get_current_user)):
    """Create a new genre"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO genres (name) VALUES (%s) RETURNING id, name",
                (genre.get("name"),)
            )
            result = cur.fetchone()
            conn.commit()
            return {"id": result[0], "name": result[1]} if result else None
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        return_connection(conn)
