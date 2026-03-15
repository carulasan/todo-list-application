import logging
from models.todo import Todo
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from typing import Union

from sqlalchemy.ext.declarative import DeclarativeMeta
from api.enums.todo import TodoStatus
from uuid import uuid4
from datetime import datetime, timedelta
import random
from api.schema.todo import TodoSchemaCreate, TodoSchemaPartialUpdate


class TodoSimpleCrudRepository:
    """Repository for creating, reading, updating or deleting Todo data in PSQL DB."""

    primary_model = Todo

    IS_NOT_DELETED = False

    class ID_Generator:
        @staticmethod
        def generate_id() -> int:
            # Simple ID generation logic (for demonstration purposes only)
            return random.randint(1, 999999999)

    def create(self, db_session: Session, record_in: TodoSchemaCreate):
        """
        Create a new Todo record in the database.
        """
        try:
            # Ensure record_in is an instance
            if not isinstance(record_in, BaseModel):
                raise TypeError(
                    f"record_in must be a Pydantic model instance, got {type(record_in)}"
                )

            # Convert Pydantic instance to dict
            record_in_dict = record_in.model_dump()  # for Pydantic v2
            record_in_dict["status"] = TodoStatus.PENDING.value

            # Create SQLAlchemy model instance
            new_todo = self.primary_model(
                **record_in_dict, id=self.ID_Generator.generate_id()
            )

            # Add to session and commit
            db_session.add(new_todo)
            db_session.commit()
            db_session.refresh(new_todo)

            return new_todo

        except Exception as e:
            db_session.rollback()
            raise e

    def update(
        self,
        db_session: Session,
        record_db: DeclarativeMeta,
        todo_update: TodoSchemaPartialUpdate,
    ):

        # Ensure the record is attached to the session
        record = db_session.merge(record_db)
        update_data = todo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)
        db_session.commit()
        return record

    def soft_delete(self, db_session: Session, record: DeclarativeMeta):
        try:
            record = db_session.merge(record)
            record.is_deleted = 1
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e

    def get_by_id(self, db_session: Session, record_id: int):
        filters = {"id": record_id, "is_deleted": self.IS_NOT_DELETED}
        queryset = db_session.query(self.primary_model).filter_by(**filters)
        record = queryset.one_or_none()
        return record

    def get_all(self, db_session: Session):
        """Retrieves all records that are not marked as deleted.

        No pagination yet

        """
        filters = {"is_deleted": self.IS_NOT_DELETED}
        queryset = db_session.query(self.primary_model).filter_by(**filters).order_by(
            self.primary_model.date_created.desc()
        )
        records = queryset.all()
        return records
