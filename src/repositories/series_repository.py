"""Series Repository con psycopg2."""
from src.repositories.base import BaseRepository


class SeriesRepository(BaseRepository):
    async def create(self, conn, obj_in: dict) -> dict:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO series (title, description) VALUES (%s, %s) RETURNING id, title, description",
                (obj_in["title"], obj_in.get("description"))
            )
            result = cur.fetchone()
            conn.commit()
            return {"id": result[0], "title": result[1], "description": result[2]} if result else None

    async def get(self, conn, id: int):
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, description FROM series WHERE id = %s", (id,))
            result = cur.fetchone()
            return {"id": result[0], "title": result[1], "description": result[2]} if result else None

    async def get_all(self, conn, skip: int = 0, limit: int = 10):
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, description FROM series ORDER BY id DESC LIMIT %s OFFSET %s",
                (limit, skip)
            )
            return [
                {"id": row[0], "title": row[1], "description": row[2]}
                for row in cur.fetchall()
            ]

    async def update(self, conn, id: int, obj_in: dict):
        fields = []
        values = []
        if obj_in.get("title") is not None:
            fields.append("title = %s")
            values.append(obj_in["title"])
        if "description" in obj_in:
            fields.append("description = %s")
            values.append(obj_in.get("description"))

        if not fields:
            return await self.get(conn, id)

        values.append(id)
        query = f"UPDATE series SET {', '.join(fields)} WHERE id = %s RETURNING id, title, description"
        with conn.cursor() as cur:
            cur.execute(query, tuple(values))
            result = cur.fetchone()
            conn.commit()
            return {"id": result[0], "title": result[1], "description": result[2]} if result else None

    async def delete(self, conn, id: int) -> bool:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM series WHERE id = %s", (id,))
            conn.commit()
            return cur.rowcount > 0
