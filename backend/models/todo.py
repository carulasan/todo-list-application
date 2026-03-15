from sqlalchemy import (
    BigInteger,
    String,
    SmallInteger,
    DateTime,
    Boolean,
    JSON,
    Index,
    ForeignKey,
    Table,
    Column,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from database.core import Base


# Association table for many-to-many relationship
todo_guest_association = Table(
    "todo_guest",
    Base.metadata,
    Column("todo_id", BigInteger, ForeignKey("todo.todo_id"), primary_key=True),
    Column("guest_id", BigInteger, ForeignKey("guest.guest_id"), primary_key=True),
)


class Guest(Base):
    __tablename__ = "guest"

    id = mapped_column("guest_id", BigInteger, primary_key=True, autoincrement=False)
    name = mapped_column("name", String(255), nullable=False)
    email = mapped_column("email", String(255), nullable=True)
    is_deleted = mapped_column("is_deleted", Boolean, nullable=False, default=False)

    # Bidirectional relationship: many guests to many todos
    todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        secondary=todo_guest_association,
        back_populates="guests",
    )

    __table_args__ = (
        Index("idx_guest_is_deleted", "is_deleted"),
        Index("idx_guest_email", "email"),
    )


class Todo(Base):
    __tablename__ = "todo"

    id = mapped_column("todo_id", BigInteger, primary_key=True, autoincrement=False)
    title = mapped_column("title", String(255), nullable=False)
    description = mapped_column("description", String, nullable=True)
    priority = mapped_column("priority", SmallInteger, nullable=False)
    status = mapped_column("status", String(50), nullable=False)
    completed_at = mapped_column("completed_at", DateTime, nullable=True)
    tags = mapped_column("tags", JSON, nullable=True)

    is_deleted = mapped_column("is_deleted", Boolean, nullable=False, default=False)

    # Bidirectional relationship: many todos to many guests
    guests: Mapped[list["Guest"]] = relationship(
        "Guest",
        secondary=todo_guest_association,
        back_populates="todos",
    )

    __table_args__ = (
        Index("idx_todo_is_deleted", "is_deleted"),
        Index("idx_todo_status", "status"),
        Index("idx_todo_priority", "priority"),
    )