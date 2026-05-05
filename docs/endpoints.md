# 📡 Series App — Endpoints

Base URL: `http://localhost:8000`  
Swagger UI: `http://localhost:8000/docs`

> 🔒 **[JWT]** requiere header: `Authorization: Bearer <token>`

---

## 🟢 Health

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/` | — | Estado de la API |
| GET | `/health` | — | Health check |

---

## 🔐 Auth — `/auth`

| Método | Ruta | Auth | Descripción | Código OK |
|--------|------|------|-------------|-----------|
| POST | `/auth/register` | — | Crear cuenta | 201 |
| POST | `/auth/login` | — | Login → JWT | 200 |
| GET | `/auth/me` | 🔒 | Perfil propio | 200 |
| PUT | `/auth/me/password` | 🔒 | Cambiar contraseña | 204 |

### POST `/auth/register`
**Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "secret123"
}
```
**Response 201:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:00:00Z"
}
```

### POST `/auth/login`
**Body:**
```json
{
  "username": "johndoe",
  "password": "secret123"
}
```
**Response 200:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": 1, "username": "johndoe", "email": "..." }
}
```

---

## 📺 Series — `/series`

| Método | Ruta | Auth | Descripción | Código OK |
|--------|------|------|-------------|-----------|
| GET | `/series` | — | Listar series | 200 |
| GET | `/series/:id` | — | Obtener serie por ID | 200 |
| POST | `/series` | 🔒 | Crear serie | 201 |
| PUT | `/series/:id` | 🔒 | Editar serie | 200 |
| DELETE | `/series/:id` | 🔒 | Eliminar serie | 204 |
| POST | `/series/:id/image` | 🔒 | Subir imagen a Cloudinary | 200 |
| DELETE | `/series/:id/image` | 🔒 | Eliminar imagen de Cloudinary | 204 |
| GET | `/series/export/csv` | — | Exportar a CSV | 200 |

---

### GET `/series` — Listado con filtros

**Query params:**

| Param | Tipo | Default | Descripción |
|-------|------|---------|-------------|
| `page` | int | `1` | Número de página |
| `limit` | int | `10` | Resultados por página (máx 100) |
| `q` | string | — | Búsqueda por título |
| `status` | string | — | `ongoing` \| `ended` \| `cancelled` \| `upcoming` |
| `genre` | string | — | Nombre del género (ej: `Drama`) |
| `year` | int | — | Filtrar por año de estreno |
| `sort` | string | `created_at` | `title` \| `release_year` \| `avg_rating` \| `created_at` |
| `order` | string | `desc` | `asc` \| `desc` |

**Ejemplos:**
```
GET /series
GET /series?page=1&limit=10
GET /series?q=breaking&sort=title&order=asc
GET /series?status=ongoing&genre=Drama
GET /series?year=2023&sort=avg_rating&order=desc
GET /series?page=2&limit=5&q=game
```

**Response 200:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Breaking Bad",
      "synopsis": "...",
      "release_year": 2008,
      "status": "ended",
      "total_seasons": 5,
      "total_episodes": 62,
      "image_url": "https://res.cloudinary.com/...",
      "genres": ["Drama", "Crime", "Thriller"],
      "avg_rating": 4.8,
      "rating_count": 312,
      "created_by": 1,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ],
  "total": 42,
  "page": 1,
  "limit": 10,
  "pages": 5
}
```

---

### GET `/series/:id`

**Response 200:**
```json
{
  "id": 1,
  "title": "Breaking Bad",
  "synopsis": "Un profesor de química...",
  "release_year": 2008,
  "status": "ended",
  "total_seasons": 5,
  "total_episodes": 62,
  "image_url": "https://res.cloudinary.com/...",
  "genres": ["Drama", "Crime"],
  "avg_rating": 4.8,
  "rating_count": 312,
  "created_by": 1,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

---

### POST `/series` 🔒

**Body:**
```json
{
  "title": "Breaking Bad",
  "synopsis": "Un profesor de química se convierte en fabricante de metanfetamina.",
  "release_year": 2008,
  "status": "ended",
  "total_seasons": 5,
  "total_episodes": 62,
  "genre_ids": [1, 3, 5]
}
```

**Response 201:** igual a GET `/series/:id`

---

### PUT `/series/:id` 🔒

Todos los campos son opcionales (PATCH semántico con PUT).

**Body:**
```json
{
  "title": "Breaking Bad (Updated)",
  "status": "ended",
  "genre_ids": [1, 3]
}
```

**Response 200:** igual a GET `/series/:id`

---

### DELETE `/series/:id` 🔒

Elimina la serie, sus ratings, géneros asociados **y la imagen de Cloudinary** si tiene una.

**Response 204:** sin body.

---

### POST `/series/:id/image` 🔒

Sube o reemplaza la imagen de portada usando Cloudinary.  
Si ya había imagen, elimina la anterior en Cloudinary antes de subir la nueva.

**Content-Type:** `multipart/form-data`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `file` | File | Imagen (JPEG, PNG, WebP, GIF) — máx 5MB |

**Response 200:**
```json
{
  "image_url": "https://res.cloudinary.com/demo/image/upload/v1/series/xk3abc123.jpg",
  "image_public_id": "series/xk3abc123"
}
```

> El backend sube a Cloudinary usando el SDK de Python (`cloudinary.uploader.upload`), guarda `image_url` e `image_public_id` en la DB, y devuelve el URL público.

---

### DELETE `/series/:id/image` 🔒

Elimina la imagen de Cloudinary (`cloudinary.uploader.destroy(public_id)`) y limpia los campos en la DB.

**Response 204:** sin body.

---

### GET `/series/export/csv`

Exporta el listado actual (acepta los mismos filtros que GET `/series` excepto paginación).

**Response 200:**
```
Content-Type: text/csv
Content-Disposition: attachment; filename=series.csv

id,title,status,release_year,genres,avg_rating,rating_count,created_at
1,Breaking Bad,ended,2008,"Drama,Crime",4.8,312,2024-01-15T10:00:00Z
```

---

## ⭐ Ratings — `/series/:id/rating`

| Método | Ruta | Auth | Descripción | Código OK |
|--------|------|------|-------------|-----------|
| POST | `/series/:id/rating` | 🔒 | Crear o actualizar rating | 201 |
| GET | `/series/:id/rating` | — | Ver todos los ratings + resumen | 200 |
| GET | `/series/:id/rating/me` | 🔒 | Ver mi rating | 200 |
| DELETE | `/series/:id/rating/me` | 🔒 | Eliminar mi rating | 204 |

### POST `/series/:id/rating` 🔒

Upsert: si el usuario ya calificó esta serie, actualiza; si no, crea.

**Body:**
```json
{
  "score": 5,
  "comment": "Una obra maestra del drama moderno."
}
```

**Response 201:**
```json
{
  "id": 7,
  "series_id": 1,
  "user_id": 2,
  "score": 5,
  "comment": "Una obra maestra del drama moderno.",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### GET `/series/:id/rating`

**Response 200:**
```json
{
  "series_id": 1,
  "avg_score": 4.8,
  "total_ratings": 312,
  "ratings": [
    {
      "id": 7,
      "user_id": 2,
      "score": 5,
      "comment": "Una obra maestra.",
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

## 🎭 Géneros — `/genres`

Catálogo de géneros. Solo lectura pública; creación requiere auth.

| Método | Ruta | Auth | Descripción | Código OK |
|--------|------|------|-------------|-----------|
| GET | `/genres` | — | Listar todos los géneros | 200 |
| POST | `/genres` | 🔒 | Crear género | 201 |
| DELETE | `/genres/:id` | 🔒 | Eliminar género | 204 |

### GET `/genres`
**Response 200:**
```json
[
  { "id": 1, "name": "Drama" },
  { "id": 2, "name": "Comedy" },
  { "id": 3, "name": "Crime" }
]
```

### POST `/genres` 🔒
**Body:**
```json
{ "name": "Sci-Fi" }
```

---

## ⚠️ Códigos HTTP usados

| Código | Cuándo |
|--------|--------|
| `200` | Lectura o actualización exitosa |
| `201` | Recurso creado |
| `204` | Eliminación exitosa (sin body) |
| `400` | Datos inválidos / archivo no permitido |
| `401` | Sin token o token expirado |
| `403` | Token válido pero sin permiso (no es dueño) |
| `404` | Recurso no encontrado |
| `409` | Conflicto (ej: username ya existe) |
| `422` | Error de validación de Pydantic |
| `500` | Error interno del servidor |

---

## 🌩️ Integración Cloudinary

Variables de entorno requeridas:

```env
CLOUDINARY_URL
```

Flujo en el backend al subir imagen:

```
POST /series/:id/image
  → recibe el archivo (multipart)
  → cloudinary.uploader.upload(file, folder="series")
  → guarda image_url + image_public_id en DB
  → retorna { image_url, image_public_id }
```

Flujo al eliminar imagen:

```
DELETE /series/:id/image  o  DELETE /series/:id
  → lee image_public_id de la DB
  → cloudinary.uploader.destroy(image_public_id)
  → limpia campos en DB
```