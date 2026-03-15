from api.schema.common import EntityCommonBase
from typing import Annotated, Optional, List
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from api.enums.todo import TodoStatus
from api.schema.common import PaginatedList


class TodoSchemaCreate(BaseModel):
    title: Annotated[str, Field(..., min_length=1, max_length=255)]
    description: Optional[str] = None
    priority: Optional[int] = Field(default=1, ge=1, le=3) 
    tags: Optional[List[str]] = None
    created_by: str = "system"


class TodoSchemaDetail(EntityCommonBase):
    id: int
    title: str
    description: Optional[str]
    priority: int
    status: str
    completed_at: Optional[datetime]
    tags: Optional[List[str]]

    model_config = ConfigDict(from_attributes=True)


class TodoList(BaseModel):
    """Todo List Response Model."""

    message: Annotated[str, Field(description="Response message")] = (
        "Retrieved Todo list."
    )
    results: Annotated[List[TodoSchemaDetail], Field(description="List of Todo")] = []

    model_config = ConfigDict(from_attributes=True)


class TodoPaginatedList(PaginatedList, TodoList):
    """Todo Paginated List Response Model."""


class TodoSchemaPartialUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    modified_by: Optional[str] = None
    date_modified: Optional[datetime] = datetime.now()
    modified_reason: Optional[str] = None
