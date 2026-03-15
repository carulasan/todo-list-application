# Geoplan Todo API Service

A FastAPI-based REST API service for managing geoplan-integrated todo lists.

## Tech Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL 11.0
- **Cache**: Redis 4.0.10
- **ORM**: SQLAlchemy
- **ASGI Server**: Uvicorn
- **Data Validation**: Pydantic
- **Frontend Framwork: Vue JS

## Prerequisites

- Docker Desktop
- Python 3.10 (for local development)

## Running the Application

1. Ensure Docker Desktop is running.
2. Navigate to the project root directory.
3. Run the following command to build and start the services:

   ```bash
   docker-compose up --build
   ```

   Or to run in detached mode:

   ```bash
   docker-compose up -d --build
   ```

4. The API will be available at `http://localhost:8004`.

## Services

- **API Service**: Runs on port 8004 (mapped to container port 8000)
- **Database**: PostgreSQL on port 5432
- **Cache**: Redis on port 6379

## Environment Variables

Copy `backend/example.env` to `backend/.env` and configure as needed.

## Development

For local development without Docker:

1. Install Python 3.10
2. Create a virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r backend/requirements.txt`
5. Run the app: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`


### Frontend

- Vue Js

## Development
For local development without docker

1. install node
2. install dependencies: `npm install`
2. Run the app `npm run dev`