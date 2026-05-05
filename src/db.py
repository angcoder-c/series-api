"""Database connection pool with psycopg2 for PostgreSQL.

Replace DATABASE_URL with real credentials or load from env/config.
"""
import psycopg2
from psycopg2 import pool
import os

# TODO: Load from environment/config securely
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/dbname")

# Connection pool para reutilizar conexiones
db_pool = psycopg2.pool.SimpleConnectionPool(
    1,  # minconn
    10,  # maxconn
    DATABASE_URL
)


def get_connection():
    """Get a connection from the pool.

    Ejemplo:
        conn = get_connection()
        cur = conn.cursor()
        try:
            ...
        finally:
            cur.close()
            conn.close()  # Devuelve la conexión al pool
    """
    return db_pool.getconn()


def return_connection(conn):
    """Return a connection to the pool."""
    if conn and db_pool:
        db_pool.putconn(conn)


def close_all_connections():
    """Close all connections in the pool (ejecutar al apagar la app)."""
    if db_pool:
        db_pool.closeall()
