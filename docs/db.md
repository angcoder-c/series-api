# Esquema de Base de Datos

El esquema está pensado para una inicialización limpia, sin `ALTER TABLE` posteriores. Todo queda creado desde el inicio en `db/schema.sql`.

---

## Tablas

### `users`
Usuarios de la aplicación.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | SERIAL | PRIMARY KEY |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE |
| `password_hash` | TEXT | NOT NULL |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |

### `genres`
Catálogo normalizado de géneros.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | SERIAL | PRIMARY KEY |
| `name` | VARCHAR(50) | NOT NULL, UNIQUE |

### `series`
Entidad principal de la aplicación.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | SERIAL | PRIMARY KEY |
| `title` | VARCHAR(200) | NOT NULL |
| `description` | TEXT | Opcional |
| `image_url` | TEXT | Opcional |
| `image_public_id` | VARCHAR(200) | Opcional |
| `release_year` | SMALLINT | Opcional |
| `status` | VARCHAR(20) | CHECK `ongoing`, `ended`, `cancelled`, `upcoming` |
| `total_seasons` | SMALLINT | CHECK `>= 0` |
| `total_episodes` | SMALLINT | CHECK `>= 0` |
| `created_by` | INTEGER | FK → `users(id)` ON DELETE SET NULL |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |

`updated_at` se mantiene con trigger en cada `UPDATE`.

### `series_genres`
Tabla de unión entre `series` y `genres`.

| Columna | Tipo | Restricciones |
|---|---|---|
| `series_id` | INTEGER | NOT NULL, FK → `series(id)` ON DELETE CASCADE |
| `genre_id` | INTEGER | NOT NULL, FK → `genres(id)` ON DELETE CASCADE |

**PK compuesta:** `(series_id, genre_id)`

### `ratings`
Valoraciones de usuarios sobre series.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | SERIAL | PRIMARY KEY |
| `series_id` | INTEGER | NOT NULL, FK → `series(id)` ON DELETE CASCADE |
| `user_id` | INTEGER | NOT NULL, FK → `users(id)` ON DELETE CASCADE |
| `score` | SMALLINT | NOT NULL, CHECK `BETWEEN 1 AND 5` |
| `comment` | TEXT | Opcional |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |

**UNIQUE:** `(series_id, user_id)`

`updated_at` también usa trigger automático.

---

## Relaciones

```text
users ──────────────────< series
users ──────────────────< ratings
series ─────────────────< ratings
series >────< series_genres >────< genres
```

---

## Índices

| Índice | Tabla | Propósito |
|---|---|---|
| `idx_series_title` | `series` | Búsqueda por título |
| `idx_series_created_by` | `series` | Filtrado por creador |
| `idx_ratings_series` | `ratings` | Consultas por serie |
| `idx_ratings_user` | `ratings` | Consultas por usuario |

---

## Notas

- El esquema es compatible con carga inicial limpia desde Docker.
- No requiere `ALTER TABLE` para agregar campos de imagen o metadatos.
- La normalización mantiene géneros y valoraciones en tablas separadas.
