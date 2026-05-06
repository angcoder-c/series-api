# Series API — Endpoints

Base URL: `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`

> `GET /auth/me` requiere `Authorization: Bearer <token>`.

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
    "description": "Un profesor de química..."
  }
]
```

### GET `/series/{series_id}`

**Response 200**

```json
{
  "id": 1,
  "title": "Breaking Bad",
  "description": "Un profesor de química..."
}
```

### POST `/series`

**Body**

```json
{
  "title": "Breaking Bad",
  "description": "Un profesor de química se convierte en fabricante de metanfetamina."
}
```

**Response 201**

```json
{
  "id": 1,
  "title": "Breaking Bad",
  "description": "Un profesor de química se convierte en fabricante de metanfetamina."
}
```

### PUT `/series/{series_id}`

**Body**

```json
{
  "title": "Breaking Bad (Updated)",
  "description": "Nueva descripción"
}
```

**Response 200**

```json
{
  "id": 1,
  "title": "Breaking Bad (Updated)",
  "description": "Nueva descripción"
}
```

### DELETE `/series/{series_id}`

**Response 200**

```json
{
  "detail": "Series deleted"
}
```