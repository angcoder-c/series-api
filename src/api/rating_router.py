"""Endpoints para ratings de series."""
from fastapi import APIRouter, HTTPException, Depends
from src.db import get_connection, return_connection
from src.schemas.dto import RatingCreate, RatingRead, RatingSummary
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/ratings", tags=["ratings"])


@router.post("", response_model=RatingRead)
async def upsert_rating(payload: RatingCreate, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    try:
        user_id = int(current_user["sub"])
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO ratings (series_id, user_id, score, comment)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (series_id, user_id)
                DO UPDATE SET
                    score = EXCLUDED.score,
                    comment = EXCLUDED.comment,
                    updated_at = NOW()
                RETURNING id, series_id, user_id, score, comment, created_at, updated_at
                """,
                (payload.series_id, user_id, payload.score, payload.comment),
            )
            result = cur.fetchone()
            conn.commit()
            if not result:
                raise HTTPException(status_code=400, detail="Could not save rating")
            return {
                "id": result[0],
                "series_id": result[1],
                "user_id": result[2],
                "score": result[3],
                "comment": result[4],
                "created_at": result[5],
                "updated_at": result[6],
            }
    finally:
        return_connection(conn)


@router.get("/series/{series_id}", response_model=RatingSummary)
async def get_series_rating_summary(series_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    try:
        user_id = int(current_user["sub"])
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COALESCE(ROUND(AVG(score)::numeric, 1), 0), COUNT(*) FROM ratings WHERE series_id = %s",
                (series_id,),
            )
            summary_row = cur.fetchone() or (0, 0)

            cur.execute(
                """
                SELECT id, series_id, user_id, score, comment, created_at, updated_at
                FROM ratings
                WHERE series_id = %s AND user_id = %s
                LIMIT 1
                """,
                (series_id, user_id),
            )
            rating_row = cur.fetchone()

            my_rating = None
            if rating_row:
                my_rating = {
                    "id": rating_row[0],
                    "series_id": rating_row[1],
                    "user_id": rating_row[2],
                    "score": rating_row[3],
                    "comment": rating_row[4],
                    "created_at": rating_row[5],
                    "updated_at": rating_row[6],
                }

            return {
                "series_id": series_id,
                "average_score": float(summary_row[0]) if summary_row[1] else None,
                "ratings_count": int(summary_row[1]),
                "my_rating": my_rating,
            }
    finally:
        return_connection(conn)