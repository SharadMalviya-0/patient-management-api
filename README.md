Patient Management API

A REST API built with FastAPI to manage patient records with auto-calculated BMI and health verdicts.

## Features
- Full CRUD operations on patient records
- Auto-calculates BMI and health verdict (underweight/normal/overweight/obese)
- Sort patients by height, weight, or BMI
- SQLite database integration using SQLAlchemy ORM
- Proper error handling with meaningful HTTP status codes
- Auto-generated API documentation via Swagger UI

## Tech Stack
- Python, FastAPI, Pydantic, SQLAlchemy, SQLite

## Project Structure
├── main.py          # API routes and Pydantic models
├── database.py      # Database connection and session setup
├── models.py        # SQLAlchemy table models
├── patients.db      # SQLite database
├── requirements.txt
└── README.md

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`

## Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /view | Get all patients |
| GET | /patient/{id} | Get a patient |
| GET | /sort | Sort patients |
| POST | /create | Add a patient |
| PUT | /edit/{id} | Update a patient |
| DELETE | /delete/{id} | Delete a patient |

## Roadmap
- [x] JSON file storage
- [x] Migrate to SQLite database
- [x] Error handling
- [ ] JWT authentication
- [ ] Dockerize the application
- [ ] Deploy on Railway/Render