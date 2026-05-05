"""User Repository con psycopg2."""
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def create(self, conn, obj_in: dict) -> dict:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id, email",
                (obj_in["email"], obj_in["password_hash"])
            )
            result = cur.fetchone()
            conn.commit()
            return {"id": result[0], "email": result[1]} if result else None

    async def get(self, conn, id: int):
        with conn.cursor() as cur:
            cur.execute("SELECT id, email FROM users WHERE id = %s", (id,))
            result = cur.fetchone()
            return {"id": result[0], "email": result[1]} if result else None

    async def get_all(self, conn, skip: int = 0, limit: int = 10):
        with conn.cursor() as cur:
            cur.execute("SELECT id, email FROM users LIMIT %s OFFSET %s", (limit, skip))
            return [{"id": r[0], "email": r[1]} for r in cur.fetchall()]

    async def get_by_email(self, conn, email: str):
        with conn.cursor() as cur:
            cur.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (email,))
            result = cur.fetchone()
            return {"id": result[0], "email": result[1], "password_hash": result[2]} if result else None

    async def update(self, conn, id: int, obj_in: dict):
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET email = %s WHERE id = %s RETURNING id, email",
                (obj_in["email"], id)
            )
            result = cur.fetchone()
            conn.commit()
            return {"id": result[0], "email": result[1]} if result else None

    async def delete(self, conn, id: int) -> bool:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (id,))
            conn.commit()
            return cur.rowcount > 0
