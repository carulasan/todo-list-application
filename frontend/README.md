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
