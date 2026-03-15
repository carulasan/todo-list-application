import re
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, SmallInteger, DateTime, func, text


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])

class CustomBaseWithDefaults:
    __repr_attrs__ = []
    __repr_max_length__ = 15

    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)

    def dict(self):
        """Returns a dict representation of a models."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # Modification Fields (Create, Update, Delete)
    created_by = mapped_column("created_by", String(250), nullable=False)
    date_created = mapped_column(
        "date_created",
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=text("CURRENT_TIMESTAMP"),
    )
    modified_by = mapped_column("modified_by", String(250))
    date_modified = mapped_column("date_modified", DateTime, onupdate=func.now())
    modified_reason = mapped_column("modified_reason", String(250))
    is_deleted = mapped_column(
        "is_deleted", SmallInteger, default=0, server_default="0"
    )


Base = declarative_base(cls=CustomBaseWithDefaults)
