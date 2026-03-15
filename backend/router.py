

from api.routers.common import router as common
from api.routers.todo import router as todo

ROOT_PREFIX = "/api"


def configure_todo_routes(app):
    """Configures Todo List Public Routes."""

    app.include_router(
        common,
        prefix=f"{ROOT_PREFIX}",
        tags=["Health"],
    )

    app.include_router(
        todo,
        prefix=f"{ROOT_PREFIX}/todo",
        tags=[f"Todo List"],
    )
