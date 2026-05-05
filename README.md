# series-api

API en FastAPI con PostgreSQL y `psycopg2`.

## Requisitos

- Python 3.12+
- PostgreSQL 16+

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Define la variable de entorno `DATABASE_URL` con tu cadena de conexión a PostgreSQL.

Ejemplo:

```bash
set DATABASE_URL=postgresql://postgres:postgres@localhost:5432/seriesdb
```

## Ejecutar la API

```bash
uvicorn main:app --reload
```

## Endpoints

- `GET /`
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`
- `GET /series`
- `GET /series/{series_id}`
- `POST /series`
- `PUT /series/{series_id}`
- `DELETE /series/{series_id}`

## Notas

- La base de datos debe estar creada antes de arrancar.
- Si usas Docker Compose desde el repo padre, el esquema se carga automáticamente con `db/schema.sql`.
