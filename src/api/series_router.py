"""Endpoints CRUD para Series."""
from fastapi import APIRouter, HTTPException
from src.db import get_connection, return_connection
from src.repositories.series_repository import SeriesRepository
from src.schemas.dto import SeriesCreate, SeriesUpdate, SeriesRead
from src.services.series_service import SeriesService

router = APIRouter(prefix="/series", tags=["series"])

series_repo = SeriesRepository()
series_service = SeriesService(series_repo)


@router.get("", response_model=list[SeriesRead])
async def list_series(skip: int = 0, limit: int = 10):
    conn = get_connection()
    try:
        return await series_service.get_all(conn, skip, limit)
    finally:
        return_connection(conn)


@router.get("/{series_id}", response_model=SeriesRead)
async def get_series(series_id: int):
    conn = get_connection()
    try:
        series = await series_service.get(conn, series_id)
        if not series:
            raise HTTPException(status_code=404, detail="Series not found")
        return series
    finally:
        return_connection(conn)


@router.post("", response_model=SeriesRead, status_code=201)
async def create_series(payload: SeriesCreate):
    conn = get_connection()
    try:
        return await series_service.create(conn, payload.model_dump())
    finally:
        return_connection(conn)


@router.put("/{series_id}", response_model=SeriesRead)
async def update_series(series_id: int, payload: SeriesUpdate):
    conn = get_connection()
    try:
        series = await series_service.update(conn, series_id, payload.model_dump(exclude_unset=True))
        if not series:
            raise HTTPException(status_code=404, detail="Series not found")
        return series
    finally:
        return_connection(conn)


@router.delete("/{series_id}")
async def delete_series(series_id: int):
    conn = get_connection()
    try:
        deleted = await series_service.delete(conn, series_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Series not found")
        return {"detail": "Series deleted"}
    finally:
        return_connection(conn)
