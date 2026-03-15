from functools import cache

from fastapi import APIRouter, Depends
from sqlalchemy import delete
from api.schema.todo import (
    TodoSchemaCreate,
    TodoSchemaDetail,
    TodoStatus,
    TodoList,
    TodoPaginatedList,
)
from api.services.todo.todo_interface import TodoInterface
from api.services.todo.todo_impl import TodoImplementation
from database.session import WriteDbSession, ReadDbSession

from api.repository.todo import TodoSimpleCrudRepository
from fastapi import HTTPException, status
from api.schema.todo import TodoSchemaPartialUpdate
from integration.redis_client import RedisCacheClient, get_cache_client
import json
from app_logger import app_logger


def get_todo_implementation() -> TodoInterface:
    return TodoImplementation(todo_repository=TodoSimpleCrudRepository())


router = APIRouter()


@router.post("/", response_model=TodoSchemaDetail, status_code=201)
def create_todo(
    todo: TodoSchemaCreate,
    db_session: WriteDbSession,
    service: TodoInterface = Depends(get_todo_implementation),
):
    response: TodoSchemaDetail = service.create_todo_item(
        db_session=db_session, todo_input=todo
    )
    return response


@router.get("/", response_model=TodoPaginatedList)
def list_todo(
    db_session: ReadDbSession, service: TodoInterface = Depends(get_todo_implementation)
):

    response: TodoPaginatedList = service.get_todo_items(db_session=db_session)
    return response


@router.get("/{todo_id}", response_model=TodoSchemaDetail)
def detail_todo(
    todo_id: int,
    db_session: ReadDbSession,
    service: TodoInterface = Depends(get_todo_implementation),
    redis_client: RedisCacheClient = Depends(get_cache_client),
):

    process_log = f"Fetch detail | todo_id={todo_id}"
    cache_todo = redis_client.get_data(key=str(todo_id))
    if cache_todo:
        app_logger.info(f"{process_log} | Found todo detail in cache.")
        return TodoSchemaDetail(**json.loads(cache_todo))

    app_logger.info(f"{process_log} | Fetch todo detail from db.")
    response: TodoSchemaDetail = service.get_detail_todo_item(
        db_session=db_session, todo_id=todo_id
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    todo_schema = TodoSchemaDetail.model_validate(response)
    redis_client.set_data(
        key=str(todo_id), value=json.dumps(todo_schema.model_dump(mode="json"))
    )
    return response


@router.patch("/{todo_id}", response_model=TodoSchemaDetail)
def partial_update_todo(
    todo_id: int,
    todo_update: TodoSchemaPartialUpdate,
    db_session: WriteDbSession,
    service: TodoInterface = Depends(get_todo_implementation),
    redis_client: RedisCacheClient = Depends(get_cache_client),
):

    redis_client.delete_data(key=str(todo_id))

    updated_todo = service.partial_update_todo_item(
        db_session=db_session, todo_update=todo_update, todo_id=todo_id
    )
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return updated_todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    db_session: WriteDbSession,
    service: TodoInterface = Depends(get_todo_implementation),
    redis_client: RedisCacheClient = Depends(get_cache_client),
):
    redis_client.delete_data(key=str(todo_id))
    service.delete_todo_item(db_session=db_session, todo_id=todo_id)
