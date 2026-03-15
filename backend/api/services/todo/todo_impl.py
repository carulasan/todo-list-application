from typing import Optional

from fastapi.background import P

from api.services.todo.todo_interface import TodoInterface
from api.schema.todo import (
    TodoSchemaCreate,
    TodoSchemaDetail,
    TodoPaginatedList,
    TodoSchemaPartialUpdate,
)
from api.repository.todo import TodoSimpleCrudRepository

from sqlalchemy.orm import Session

class TodoImplementation(TodoInterface):

    def __init__(self, todo_repository: TodoSimpleCrudRepository):
        self.todo_repository = todo_repository

    def create_todo_item(self, db_session: Session, todo_input: TodoSchemaCreate):
        db_created = self.todo_repository.create(
            db_session=db_session, record_in=todo_input
        )
        return db_created

    def get_todo_items(self, db_session: Session):

        todos = self.todo_repository.get_all(db_session=db_session)
        response = {
            "message": "Retrieved todo list.",
            "results": todos,
            "count": 1,
            "total_pages": 1,
            "page": 1,
            "per_page": 10,
        }

        return response

    def get_detail_todo_item(
        self, db_session: Session, todo_id: int
    ) -> TodoSchemaDetail:
        todo = self.todo_repository.get_by_id(db_session=db_session, record_id=todo_id) 
        return todo

    def partial_update_todo_item(
        self, db_session: Session, todo_update: TodoSchemaPartialUpdate, todo_id: int
    ) -> Optional[TodoSchemaDetail]:
        record_db = self.todo_repository.get_by_id(
            db_session=db_session, record_id=todo_id
        )
        if not record_db:
            return None

        record_db = self.todo_repository.update(
            db_session=db_session, record_db=record_db, todo_update=todo_update
        )
        return record_db

    def delete_todo_item(self, db_session: Session, todo_id: int):
        record_db = self.todo_repository.get_by_id(
            db_session=db_session, record_id=todo_id
        )
        if not record_db:
            return
        self.todo_repository.soft_delete(db_session=db_session, record=record_db)
