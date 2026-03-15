from datetime import datetime
from fastapi import status
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Annotated


class EntityCommonBase(BaseModel):
    """Entity Common Base Model for Date Creation/Modification."""

    created_by: Annotated[str, Field(description="Creator")] 
    date_created: Annotated[datetime, Field(description="Creation date")]
    modified_by: Annotated[Optional[str], Field(description="Modifier")] = None
    date_modified: Annotated[Optional[datetime], Field(description="Modification date")] = None
    modified_reason: Annotated[
        Optional[str], Field(description="Reason for modification")
    ] = None


class PaginatedList(BaseModel):
    """Paginated List Response Model."""

    page: Annotated[int, Field(description="Current page number")] = 0
    per_page: Annotated[int, Field(description="Items per page")] = 10
    total_count: Annotated[int, Field(default=0, description="Total item count")] = 0
    total_pages: Annotated[int, Field(default=0, description="Total pages count")] = 0


class Response(BaseModel):
    """ Generic Service Response  """
    is_success: bool = False
    details: dict = {}
