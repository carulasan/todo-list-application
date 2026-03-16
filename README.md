# Geoplan Todo List Application

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

## Running the Application both Frontend and backend via Dockerize Container

1. Ensure Docker Desktop is running.
2. Navigate to the project root directory.
3. Environment Variables
   Copy `backend/.env.example` to `backend/.env` and configure as needed.
4. Run the following command to build and start the services:

   ```bash
   docker-compose up --build
   ```

   Or to run in detached mode:

   ```bash
   docker-compose up -d --build
   ```

5. The API will be available at `http://localhost:8004`.
   Then Frontend will be available at `http://localhost:3000`

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



# Frontend Application
# Geoplan Todo Frontend

A Vue.js 3 todo application for managing tasks.

## Features

- ✅ Create, read, update, and delete tasks
- 🎯 Set task priority (low, medium, high)
- 📝 Add task descriptions
- ✓ Mark tasks as completed
- 📊 View task statistics
- 🎨 Modern, responsive UI

## Prerequisites

- Node.js 16+ 
- npm or yarn

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

The frontend will proxy API requests to `http://localhost:8000` (backend).

## Build

Build for production:
```bash
npm run build
```

## Project Structure

```
src/
├── main.js              # Vue app entry point
├── App.vue              # Main app component
├── api/
│   └── todoService.js   # API service for backend communication
└── components/
    ├── TodoForm.vue     # Form to create new tasks
    ├── TodoList.vue     # Display list of tasks
    └── TodoEditModal.vue # Modal to edit tasks
```

## Configuration

The API base URL is configured in `src/api/todoService.js`. Update it to match your backend URL if needed.

## Technologies Used

- **Vue.js 3** - Progressive JavaScript framework
- **Vite** - Frontend build tool and dev server
- **Axios** - HTTP client for API requests