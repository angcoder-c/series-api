# Esquema de Base de Datos

Normalizado hasta **3FN** y alineado con el schema real de `db/schema.sql`.

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

---

### `genres`
Catálogo normalizado de géneros.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | SERIAL | PRIMARY KEY |
| `name` | VARCHAR(50) | NOT NULL, UNIQUE |

---

### `series`
Entidad principal.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | SERIAL | PRIMARY KEY |
| `title` | VARCHAR(200) | NOT NULL |
| `description` | TEXT |  |
| `created_by` | INTEGER | FK → `users(id)` ON DELETE SET NULL |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |

---

### `series_genres`
Tabla de unión entre `series` y `genres`.

| Columna | Tipo | Restricciones |
|---|---|---|
| `series_id` | INTEGER | NOT NULL, FK → `series(id)` ON DELETE CASCADE |
| `genre_id` | INTEGER | NOT NULL, FK → `genres(id)` ON DELETE CASCADE |

**PK compuesta:** `(series_id, genre_id)`

---

### `ratings`
Rating de un usuario sobre una serie.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | SERIAL | PRIMARY KEY |
| `series_id` | INTEGER | NOT NULL, FK → `series(id)` ON DELETE CASCADE |
| `user_id` | INTEGER | NOT NULL, FK → `users(id)` ON DELETE CASCADE |
| `score` | SMALLINT | NOT NULL, CHECK (score BETWEEN 1 AND 5) |
| `comment` | TEXT |  |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() |

**UNIQUE:** `(series_id, user_id)`

---

## Relaciones

```text
users ──────────────────< series
users ──────────────────< ratings
series ─────────────────< ratings
series >────< series_genres >────< genres
```

---

## Justificación

| Forma Normal | Detalle |
|---|---|
| **1FN** | No hay grupos repetidos. Los géneros están en una tabla aparte. |
| **2FN** | `series_genres` depende de su PK compuesta completa. |
| **3FN** | No hay dependencias transitivas. Cada tabla guarda solo atributos que dependen de su clave primaria. |
