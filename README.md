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
- uv / pip

---

## Local Project Setup

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone [https://github.com/Miar0/Django_REST_Course.git](https://github.com/Miar0/Django_REST_Course.git)
   cd Django_REST_Course
   ```

2. Create and activate a virtual environment using `uv`:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install project dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Create the `.env` configuration file based on the provided template:
   ```bash
   cp .env.example .env
   ```

5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

6. Populate the database with initial sample data using the custom `seed` command:
   ```bash
   python manage.py seed
   ```

7. Start the local development server:
   ```bash
   python manage.py runserver
   ```

8. Run automated tests (optional):
   ```bash
   python manage.py test courses
   ```

---

## Running with Docker

The project includes pre-configured `Dockerfile` and `docker-compose.yaml` files for containerized execution.

1. Ensure your `.env` file exists:
   ```bash
   cp .env.example .env
   ```

2. Build and start the containers:
   ```bash
   docker compose up --build
   ```
   *(Database migrations will apply automatically upon startup).*

3. (Optional) Populate the database with initial seed data:
   ```bash
   docker compose exec web python manage.py seed
   ```

4. (Optional) Run tests inside the container:
   ```bash
   docker compose exec web python manage.py test courses
   ```

The application will be accessible at: `http://127.0.0.1:8000/api/`

---

## Authentication & Authorization (JWT)

Authentication is handled via JSON Web Tokens (`djangorestframework-simplejwt`).

To access protected endpoints:
1. Obtain tokens by sending credentials to `/api/token/`.
2. Include the access token in the `Authorization` request header:
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