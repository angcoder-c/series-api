# series-api

[![FastAPI](https://img.shields.io/badge/FastAPI-0.136.1-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![psycopg2](https://img.shields.io/badge/psycopg2-binary-important)](https://www.psycopg.org/docs/)

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

## Documentación

- [Endpoints](docs/endpoints.md)
- [Base de datos](docs/db.md)
- [Guía del entorno Docker](../README.md)

## Notas

- La base de datos debe estar creada antes de arrancar.
- Si usas Docker Compose desde el repo padre, el esquema se carga automáticamente con `db/schema.sql`.
