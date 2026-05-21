# Workout Tracker API

A REST API for managing workouts, tracking progress, and generating reports. 
Built with FastAPI and PostgreSQL, featuring JWT authentication, a seeded exercise 
library, workout scheduling with status transitions, and aggregate reporting on 
training volume and progression over time.

## Tech Stack

- Python, FastAPI, SQLAlchemy, PostgreSQL
- JWT Authentication, bcrypt
- Alembic migrations
- Docker, Docker Compose
- pytest

## Setup

1. Clone the repository
2. Create a virtual environment and activate it
```bash
   python -m venv venv
   source venv/bin/activate
```
3. Install dependencies
```bash
   pip install -r requirements.txt
```
4. Create a `.env` file based on `.env.example` and fill in your values
5. Run migrations
```bash
   alembic upgrade head
```
6. Seed exercises
```bash
   python -m scripts.seed_exercises
```
7. Start the server
```bash
   uvicorn src.main:app --reload
```

## Running Tests

Create a test database with the same name as your main database suffixed with `_test`, then run:

```bash
pytest -v -s
```
The test suite covers 77 tests across auth, exercises, workouts, scheduled workouts, workout logs, and reports.

## Running with Docker

1. Create a `.env.docker` file based on `.env.docker.example`
2. Start the containers
```bash
   docker-compose up --build
```
3. Run migrations
```bash
   docker-compose exec api alembic upgrade head
```
4. Seed exercises
```bash
   docker-compose exec api python -m scripts.seed_exercises
```
5. API available at `http://localhost:8000`

## API Reference

Interactive docs available at `http://localhost:8000/docs` after starting the server.

### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | No | Create account |
| POST | /auth/login | No | Get JWT token |

### Exercises
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /exercises | No | List all exercises, filter by category/muscle_group |
| GET | /exercises/{id} | No | Get one exercise |
| POST | /exercises | Yes | Create custom exercise |
| PUT | /exercises/{id} | Yes | Update own exercise |
| DELETE | /exercises/{id} | Yes | Delete own exercise |

### Workouts
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /workouts | Yes | Create workout with exercises |
| GET | /workouts | Yes | List own workouts |
| GET | /workouts/{id} | Yes | Get one workout |
| PUT | /workouts/{id} | Yes | Update workout |
| DELETE | /workouts/{id} | Yes | Delete workout |
| POST | /workouts/{id}/schedule | Yes | Schedule a workout |
| GET | /workouts/scheduled | Yes | List scheduled workouts |
| GET | /workouts/scheduled/{id} | Yes | Get one scheduled workout |
| PATCH | /workouts/scheduled/{id}/status | Yes | Update scheduled workout status |
| DELETE | /workouts/scheduled/{id} | Yes | Delete scheduled workout |
| POST | /workouts/logs | Yes | Log a completed workout |
| POST | /workouts/logs/{id}/exercises | Yes | Add exercises to a log |

### Reports
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /reports/summary | Yes | Workout summary and stats |
| GET | /reports/progress/{exercise_id} | Yes | Progress tracking for an exercise |

## Key Features

- JWT authentication with protected routes
- Full CRUD for workout plans with nested exercises
- Workout scheduling with status transitions (pending → active → completed/cancelled)
- Workout logging - track actual performance vs planned
- Reports - total volume, weekly frequency, per-exercise progression over time
- Custom exercises per user alongside seeded exercise library
- Database migrations with Alembic
- Containerized with Docker and Docker Compose