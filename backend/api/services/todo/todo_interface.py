from abc import ABC, abstractmethod
from api.schema.todo import TodoSchemaDetail, TodoPaginatedList, TodoSchemaCreate
from sqlalchemy.orm import Session
from api.repository.todo import TodoSimpleCrudRepository
from api.schema.todo import TodoSchemaPartialUpdate


class TodoInterface(ABC):

    @abstractmethod
    def create_todo_item(self, db_session: Session, todo_input) -> TodoSchemaDetail:
        """Creates a new todo item."""
        pass

    @abstractmethod
    def get_todo_items(self, db_session: Session) -> TodoPaginatedList:
        """Retrieves a list of all todo items."""
        pass

    @abstractmethod
    def get_detail_todo_item(
        self, db_session: Session, todo_id: int
    ) -> TodoSchemaDetail:
        """Retrieves details of a specific todo item."""
        pass

    @abstractmethod
    def partial_update_todo_item(
        self, db_session: Session, todo_update: TodoSchemaPartialUpdate, todo_id: int
    ) -> TodoSchemaDetail:
        """Partially updates an existing todo item."""
        pass

    @abstractmethod
    def delete_todo_item(self, db_session: Session, todo_id: int):
        """Deletes a specific todo item."""
        pass
