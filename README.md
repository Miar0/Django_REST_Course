# Course Platform API

A REST API service for managing courses, tags, and lessons built with Django and Django REST Framework. Features full CRUD operations via ViewSets, JWT authentication (SimpleJWT), query filtering, search, pagination, and object-level permission control.

## Requirements & Tech Stack

- Python 3.12+
- Django 6+
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- django-environ
- Docker & Docker Compose
- uv (Package & Project Management via `pyproject.toml`)

---

## Local Project Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Miar0/Django_REST_Course.git](https://github.com/Miar0/Django_REST_Course.git)
cd Django_REST_Course
```

### 2. Check or Install `uv`
Verify whether `uv` is already installed on your system:
```bash
uv --version
```

If it is not installed, install it using the official standalone installer:

- **macOS & Linux:**
  ```bash
  curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
  ```

- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
  ```

> *Note: After installation, restart your terminal or source your shell profile so that `uv` is added to your `PATH`.*

### 3. Install Dependencies & Set Up Environment
`uv` automatically creates and manages the virtual environment (`.venv`) and installs all dependencies specified in `pyproject.toml`:

```bash
uv sync
```

You can activate the virtual environment manually (`source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\activate` on Windows), or simply run commands prefixed with `uv run`.

### 4. Environment Configuration
Create the `.env` configuration file based on the provided template:
```bash
cp .env.example .env
```

### 5. Apply Database Migrations
```bash
uv run python manage.py migrate
```

### 6. (Optional) Populate Database with Sample Data
Populate the database with initial dummy records using the custom `seed` management command:
```bash
uv run python manage.py seed
```

### 7. Start the Development Server
```bash
uv run python manage.py runserver
```

### 8. Run Automated Tests
```bash
uv run python manage.py test courses
```

---

## Running with Docker

The project includes a pre-configured `Dockerfile` and `docker-compose.yaml` for containerized development.

1. Ensure your `.env` file exists:
   ```bash
   cp .env.example .env
   ```

2. Build and start the containers:
   ```bash
   docker compose up --build
   ```
   *(Database migrations are applied automatically on startup).*

3. (Optional) Populate the database with initial seed data:
   ```bash
   docker compose exec web python manage.py seed
   ```

4. (Optional) Run the test suite inside the running container:
   ```bash
   docker compose exec web python manage.py test courses
   ```

The application will be accessible at: `http://127.0.0.1:8000/api/`

---

## Authentication & Authorization (JWT)

Authentication is handled via JSON Web Tokens (`djangorestframework-simplejwt`).

To access protected endpoints:
1. Obtain token pairs by posting user credentials to `/api/token/`.
2. Include the access token in the `Authorization` HTTP header:
   ```http
   Authorization: Bearer <your_access_token>
   ```
3. Requests without a valid token to protected endpoints return `401 Unauthorized` with a `WWW-Authenticate: Bearer` challenge header.

---

## API Endpoints Table

| Method | Endpoint | Description | Permissions |
|---|---|---|---|
| **Authentication** | | | |
| POST | `/api/token/` | Obtain JWT pair (`access` and `refresh`) | AllowAny |
| POST | `/api/token/refresh/` | Refresh expired access token | AllowAny |
| POST | `/api/token/verify/` | Verify token validity | AllowAny |
| GET | `/api/me/` | Get current authenticated user profile | IsAuthenticated |
| **Courses** | | | |
| GET | `/api/courses/` | Retrieve a list of courses (filtering, search, pagination) | AllowAny |
| POST | `/api/courses/` | Create a new course (assigns current user as owner) | IsAuthenticated |
| GET | `/api/courses/<id>/` | Retrieve course details | AllowAny |
| PUT | `/api/courses/<id>/` | Full update of a course | Course Owner or Staff |
| PATCH | `/api/courses/<id>/` | Partial update of a course | Course Owner or Staff |
| DELETE | `/api/courses/<id>/` | Delete a course | Course Owner or Staff |
| GET | `/api/courses/free/` | List all free courses (`price == 0`) | AllowAny |
| **Lessons** | | | |
| GET | `/api/lessons/` | Retrieve lessons list (filters by `course`, `order`) | AllowAny |
| POST | `/api/lessons/` | Add a lesson to a course (only course owner can add) | Course Owner or Staff |
| GET | `/api/lessons/<id>/` | Retrieve lesson details | AllowAny |
| PUT/PATCH | `/api/lessons/<id>/` | Update lesson details | Course Owner or Staff |
| DELETE | `/api/lessons/<id>/` | Delete a lesson | Course Owner or Staff |
| **Tags** | | | |
| GET | `/api/tags/` | List available tags (reference dictionary) | Read-only (AllowAny) |
| GET | `/api/tags/<id>/` | Retrieve tag details | Read-only (AllowAny) |

---

## Filtering, Search, and Ordering

- **Search**: `?search=python` (searches across course title, description, and related tag names).
- **Filtering**: `?tags=1` (filter courses by tag ID), `?owner=2`, `?course=1` (for lessons).
- **Ordering**: `?ordering=price` (ascending), `?ordering=-date_start` (descending by start date).
- **Pagination**: `?page=2` (default page size is set to 10 items).