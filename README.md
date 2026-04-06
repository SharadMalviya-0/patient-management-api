# Patient Management API

A REST API built with FastAPI to manage patient records with auto-calculated BMI and health verdicts.

## Features
- Full CRUD operations on patient records
- Auto-calculates BMI and health verdict (underweight/normal/overweight/obese)
- Sort patients by height, weight, or BMI
- Data stored in JSON file

## Tech Stack
- Python, FastAPI, Pydantic

## Run Locally
```bash
pip install fastapi uvicorn
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
- [ ] Migrate to PostgreSQL database
- [ ] Add JWT authentication
- [ ] Dockerize the application
- [ ] Deploy on Railway/Render
