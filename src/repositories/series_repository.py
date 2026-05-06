"""Series Repository con psycopg2."""
from src.repositories.base import BaseRepository


class SeriesRepository(BaseRepository):
    async def create(self, conn, obj_in: dict) -> dict:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO series (title, description, image_url, image_public_id, release_year, status, total_seasons, total_episodes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, title, description, image_url, image_public_id, release_year, status, total_seasons, total_episodes",
                (
                    obj_in["title"],
                    obj_in.get("description"),
                    obj_in.get("image_url"),
                    obj_in.get("image_public_id"),
                    obj_in.get("release_year"),
                    obj_in.get("status"),
                    obj_in.get("total_seasons"),
                    obj_in.get("total_episodes")
                )
            )
            result = cur.fetchone()
            conn.commit()
            return {
                "id": result[0],
                "title": result[1],
                "description": result[2],
                "image_url": result[3],
                "image_public_id": result[4],
                "release_year": result[5],
                "status": result[6],
                "total_seasons": result[7],
                "total_episodes": result[8]
            } if result else None

    async def get(self, conn, id: int):
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, description, image_url, image_public_id, release_year, status, total_seasons, total_episodes FROM series WHERE id = %s", (id,))
            result = cur.fetchone()
            return {
                "id": result[0],
                "title": result[1],
                "description": result[2],
                "image_url": result[3],
                "image_public_id": result[4],
                "release_year": result[5],
                "status": result[6],
                "total_seasons": result[7],
                "total_episodes": result[8]
            } if result else None

    async def get_all(self, conn, skip: int = 0, limit: int = 10):
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, description, image_url, image_public_id, release_year, status, total_seasons, total_episodes FROM series ORDER BY id DESC LIMIT %s OFFSET %s",
                (limit, skip)
            )
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "image_url": row[3],
                    "image_public_id": row[4],
                    "release_year": row[5],
                    "status": row[6],
                    "total_seasons": row[7],
                    "total_episodes": row[8]
                }
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
        if "image_url" in obj_in:
            fields.append("image_url = %s")
            values.append(obj_in.get("image_url"))
        if "image_public_id" in obj_in:
            fields.append("image_public_id = %s")
            values.append(obj_in.get("image_public_id"))
        if "release_year" in obj_in:
            fields.append("release_year = %s")
            values.append(obj_in.get("release_year"))
        if "status" in obj_in:
            fields.append("status = %s")
            values.append(obj_in.get("status"))
        if "total_seasons" in obj_in:
            fields.append("total_seasons = %s")
            values.append(obj_in.get("total_seasons"))
        if "total_episodes" in obj_in:
            fields.append("total_episodes = %s")
            values.append(obj_in.get("total_episodes"))

        if not fields:
            return await self.get(conn, id)

        values.append(id)
        query = f"UPDATE series SET {', '.join(fields)} WHERE id = %s RETURNING id, title, description, image_url, image_public_id, release_year, status, total_seasons, total_episodes"
        with conn.cursor() as cur:
            cur.execute(query, tuple(values))
            result = cur.fetchone()
            conn.commit()
            return {
                "id": result[0],
                "title": result[1],
                "description": result[2],
                "image_url": result[3],
                "image_public_id": result[4],
                "release_year": result[5],
                "status": result[6],
                "total_seasons": result[7],
                "total_episodes": result[8]
            } if result else None

    async def delete(self, conn, id: int) -> bool:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM series WHERE id = %s", (id,))
            conn.commit()
            return cur.rowcount > 0
