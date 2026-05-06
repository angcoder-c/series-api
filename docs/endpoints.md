# Series API — Endpoints

Base URL: `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`

> `GET /auth/me` requiere `Authorization: Bearer <token>`.
>
> `POST /genres` requiere autenticación Bearer.

---

## Health

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Estado básico de la API |

---

## Auth — `/auth`

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/signup` | No | Registrar usuario |
| POST | `/auth/login` | No | Obtener JWT |
| GET | `/auth/me` | Sí | Obtener perfil del usuario autenticado |

### POST `/auth/signup`

**Body**

```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response 200**

```json
{
  "id": 1,
  "email": "john@example.com"
}
```

### POST `/auth/login`

**Body**

```json
{
  "email": "john@example.com",
  "password": "secret123"
}
```

**Response 200**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### GET `/auth/me`

**Headers**

```http
Authorization: Bearer eyJ...
```

**Response 200**

```json
{
  "id": 1,
  "email": "john@example.com"
}
```

---

## Series — `/series`

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/series` | No | Listar series |
| GET | `/series/{series_id}` | No | Obtener una serie por ID |
| POST | `/series` | No | Crear una serie |
| POST | `/series/upload-image` | No | Subir imagen a Cloudinary |
| PUT | `/series/{series_id}` | No | Actualizar una serie |
| DELETE | `/series/{series_id}` | No | Eliminar una serie |

### GET `/series`

**Query params**

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `skip` | int | `0` | Cantidad de registros a saltar |
| `limit` | int | `10` | Cantidad máxima de registros |

**Response 200**

```json
[
  {
    "id": 1,
    "title": "Breaking Bad",
    "description": "Un profesor de química...",
    "image_url": "https://res.cloudinary.com/.../image/upload/...jpg",
    "image_public_id": "series-app/abc123",
    "release_year": 2008,
    "status": "ended",
    "total_seasons": 5,
    "total_episodes": 62
  }
]
```

### GET `/series/{series_id}`

**Response 200**

```json
{
  "id": 1,
  "title": "Breaking Bad",
  "description": "Un profesor de química...",
  "image_url": "https://res.cloudinary.com/.../image/upload/...jpg",
  "image_public_id": "series-app/abc123",
  "release_year": 2008,
  "status": "ended",
  "total_seasons": 5,
  "total_episodes": 62
}
```

### POST `/series`

**Body**

```json
{
  "title": "Breaking Bad",
  "description": "Un profesor de química se convierte en fabricante de metanfetamina.",
  "image_url": "https://res.cloudinary.com/.../image/upload/...jpg",
  "image_public_id": "series-app/abc123",
  "release_year": 2008,
  "status": "ended",
  "total_seasons": 5,
  "total_episodes": 62
}
```

**Response 201**

```json
{
  "id": 1,
  "title": "Breaking Bad",
  "description": "Un profesor de química se convierte en fabricante de metanfetamina.",
  "image_url": "https://res.cloudinary.com/.../image/upload/...jpg",
  "image_public_id": "series-app/abc123",
  "release_year": 2008,
  "status": "ended",
  "total_seasons": 5,
  "total_episodes": 62
}
```

### POST `/series/upload-image`

**Body** (`multipart/form-data`)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `file` | archivo | Imagen a subir |

**Response 200**

```json
{
  "image_url": "https://res.cloudinary.com/.../image/upload/...jpg",
  "image_public_id": "series-app/abc123"
}
```

### PUT `/series/{series_id}`

**Body**

```json
{
  "title": "Breaking Bad (Updated)",
  "description": "Nueva descripción",
  "image_url": "https://res.cloudinary.com/.../image/upload/...jpg",
  "image_public_id": "series-app/abc123",
  "release_year": 2008,
  "status": "ended",
  "total_seasons": 5,
  "total_episodes": 62
}
```

**Response 200**

```json
{
  "id": 1,
  "title": "Breaking Bad (Updated)",
  "description": "Nueva descripción",
  "image_url": "https://res.cloudinary.com/.../image/upload/...jpg",
  "image_public_id": "series-app/abc123",
  "release_year": 2008,
  "status": "ended",
  "total_seasons": 5,
  "total_episodes": 62
}
```

### DELETE `/series/{series_id}`

**Response 200**

```json
{
  "detail": "Series deleted"
}
```

---

## Genres — `/genres`

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/genres` | No | Listar géneros |
| POST | `/genres` | Sí | Crear un género |

### GET `/genres`

**Response 200**

```json
[
  {
    "id": 1,
    "name": "Drama"
  },
  {
    "id": 2,
    "name": "Crimen"
  }
]
```

### POST `/genres`

**Headers**

```http
Authorization: Bearer eyJ...
Content-Type: application/json
```

**Body**

```json
{
  "name": "Thriller"
}
```

**Response 200**

```json
{
  "id": 3,
  "name": "Thriller"
}
```

---

## Ratings — `/ratings`

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/ratings` | Sí | Crear o actualizar una calificación |
| GET | `/ratings/series/{series_id}` | Sí | Ver resumen de calificaciones de una serie |

### POST `/ratings`

**Headers**

```http
Authorization: Bearer eyJ...
Content-Type: application/json
```

**Body**

```json
{
  "series_id": 1,
  "score": 5,
  "comment": "Muy buena serie"
}
```

**Response 200**

```json
{
  "id": 1,
  "series_id": 1,
  "user_id": 1,
  "score": 5,
  "comment": "Muy buena serie",
  "created_at": "2026-05-05T12:00:00Z",
  "updated_at": "2026-05-05T12:00:00Z"
}
```

### GET `/ratings/series/{series_id}`

**Headers**

```http
Authorization: Bearer eyJ...
```

**Response 200**

```json
{
  "series_id": 1,
  "average_score": 4.5,
  "ratings_count": 8,
  "my_rating": {
    "id": 1,
    "series_id": 1,
    "user_id": 1,
    "score": 5,
    "comment": "Muy buena serie",
    "created_at": "2026-05-05T12:00:00Z",
    "updated_at": "2026-05-05T12:00:00Z"
  }
}
```
