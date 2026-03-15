from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from settings import system_settings
from router import configure_todo_routes

environment = system_settings.ENV
options = {
    "openapi_url": "/api/v1/openapi.json" if environment != "production" else None
}

app = FastAPI(**options)


# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
configure_todo_routes(app)