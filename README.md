# Course Platform API

A REST API service for managing courses, tags, and lessons built with Django and Django REST Framework. Features full CRUD operations via ViewSets, query filtering, search, pagination, and object-level permission control.

## Requirements & Tech Stack

- Python 3.12+
- Django 6+
- Django REST Framework
- django-filter
- django-environ
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

## API Endpoints Table

| Method | Endpoint | Description | Permissions |
|---|---|---|---|
| GET | `/api/courses/` | Retrieve a list of courses (supports filtering, search, and pagination) | AllowAny |
| POST | `/api/courses/` | Create a new course | IsAuthenticated |
| GET | `/api/courses/<id>/` | Retrieve course details | AllowAny |
| PUT | `/api/courses/<id>/` | Full update of a course | Owner or Admin |
| PATCH | `/api/courses/<id>/` | Partial update of a course | Owner or Admin |
| DELETE | `/api/courses/<id>/` | Delete a course | Owner or Admin |
| GET | `/api/courses/free/` | List all free courses (`price == 0`) | AllowAny |
| GET | `/api/tags/` | List available tags (reference dictionary) | Read-only (AllowAny) |
| GET | `/api/tags/<id>/` | Retrieve tag details | Read-only (AllowAny) |
| GET | `/api/lessons/` | Retrieve lessons list (filters by `course`, `order`) | AllowAny |
| POST | `/api/lessons/` | Add a new lesson to a course | IsAuthenticated |
| GET | `/api/lessons/<id>/` | Retrieve lesson details | AllowAny |
| PATCH/PUT | `/api/lessons/<id>/` | Update lesson details | Course Owner or Admin |
| DELETE | `/api/lessons/<id>/` | Delete a lesson | Course Owner or Admin |

---

## Filtering, Search, and Ordering

- **Search**: `?search=python` (searches across course title, description, and related tag names).
- **Filtering**: `?tags=1` (filter courses by tag ID), `?owner=2`.
- **Ordering**: `?ordering=price` (ascending by price), `?ordering=-date_start` (descending by start date).
- **Pagination**: `?page=2` (default page size is set to 10 items).