# Esquema de Base de Datos

Normalizado hasta **3FN**.

---

## Tablas

### `users`
Usuarios de la aplicación.

| Columna           | Tipo          | Restricciones                  |
|-------------------|---------------|--------------------------------|
| `id`              | SERIAL        | PRIMARY KEY                    |
| `username`        | VARCHAR(50)   | NOT NULL, UNIQUE               |
| `email`           | VARCHAR(100)  | NOT NULL, UNIQUE               |
| `hashed_password` | TEXT          | NOT NULL                       |
| `is_active`       | BOOLEAN       | NOT NULL, DEFAULT TRUE         |
| `created_at`      | TIMESTAMPTZ   | NOT NULL, DEFAULT NOW()        |

---

### `genres`
Catálogo normalizado de géneros. Se separa de `series` para evitar redundancia y anomalías de actualización (viola 2FN si se guarda como texto repetido).

| Columna  | Tipo        | Restricciones       |
|----------|-------------|---------------------|
| `id`     | SERIAL      | PRIMARY KEY         |
| `name`   | VARCHAR(50) | NOT NULL, UNIQUE    |

---

### `series`
Entidad principal. Cada atributo depende únicamente de `id` (cumple 3FN).

| Columna           | Tipo         | Restricciones                                               |
|-------------------|--------------|-------------------------------------------------------------|
| `id`              | SERIAL       | PRIMARY KEY                                                 |
| `title`           | VARCHAR(200) | NOT NULL                                                    |
| `synopsis`        | TEXT         |                                                             |
| `release_year`    | SMALLINT     |                                                             |
| `status`          | VARCHAR(20)  | CHECK IN ('ongoing','ended','cancelled','upcoming')         |
| `total_seasons`   | SMALLINT     |                                                             |
| `total_episodes`  | SMALLINT     |                                                             |
| `image_url`       | TEXT         | URL pública de Cloudinary                                   |
| `image_public_id` | VARCHAR(200) | ID interno de Cloudinary (para borrar/reemplazar)          |
| `created_by`      | INTEGER      | NOT NULL, FK → users(id)                                    |
| `created_at`      | TIMESTAMPTZ  | NOT NULL, DEFAULT NOW()                                     |
| `updated_at`      | TIMESTAMPTZ  | NOT NULL, DEFAULT NOW()                                     |

> `image_public_id` se guarda porque Cloudinary requiere el `public_id` para eliminar o transformar una imagen, no el URL.

---

### `series_genres`
Tabla de unión entre `series` y `genres`. Una serie puede tener varios géneros (N:M).

| Columna    | Tipo    | Restricciones                          |
|------------|---------|----------------------------------------|
| `series_id`| INTEGER | NOT NULL, FK → series(id) ON DELETE CASCADE |
| `genre_id` | INTEGER | NOT NULL, FK → genres(id) ON DELETE CASCADE |

**PK compuesta:** `(series_id, genre_id)`

> Extraer esta relación a su propia tabla evita grupos repetidos en `series`, cumpliendo **1FN**.

---

### `ratings`
Rating de un usuario sobre una serie. Un usuario solo puede calificar una serie una vez (restricción UNIQUE).

| Columna     | Tipo        | Restricciones                                    |
|-------------|-------------|--------------------------------------------------|
| `id`        | SERIAL      | PRIMARY KEY                                      |
| `series_id` | INTEGER     | NOT NULL, FK → series(id) ON DELETE CASCADE      |
| `user_id`   | INTEGER     | NOT NULL, FK → users(id) ON DELETE CASCADE       |
| `score`     | SMALLINT    | NOT NULL, CHECK (score BETWEEN 1 AND 5)          |
| `comment`   | TEXT        |                                                  |
| `created_at`| TIMESTAMPTZ | NOT NULL, DEFAULT NOW()                          |
| `updated_at`| TIMESTAMPTZ | NOT NULL, DEFAULT NOW()                          |

**UNIQUE:** `(series_id, user_id)`

---

## Relaciones

```
users ──────────────────< series          (1:N — un user crea muchas series)
users ──────────────────< ratings         (1:N — un user deja muchos ratings)
series ─────────────────< ratings         (1:N — una serie tiene muchos ratings)
series >────< series_genres >────< genres (N:M — una serie tiene varios géneros)
```

---

## Justificación de normalización

| Forma Normal | Detalle |
|---|---|---|
| **1FN** | Sin grupos repetidos. Los géneros van en tabla separada `series_genres`. |
| **2FN** | Todas las columnas de `series_genres` dependen de la PK compuesta completa. No hay dependencias parciales. |
| **3FN** | Sin dependencias transitivas. `genres` separado evita que `genre_name` dependa de `genre_id` dentro de `series`. `image_public_id` e `image_url` dependen directamente de `series.id`, no entre sí. |