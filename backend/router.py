from api.routers import todo


ROOT_PREFIX = "/api"


def configure_todo_routes(app):
    """Configures Todo List Public Routes."""

    app.include_router(
        todo.router,
        prefix=f"{ROOT_PREFIX}/todo",
        tags=[f"Todo List"],
    )
