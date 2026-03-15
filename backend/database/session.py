import time
from uuid import uuid4
from contextlib import contextmanager
from typing import Annotated, Generator
from fastapi import Depends
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

from settings import db_settings
from app_logger import app_logger as logger


# DB Read and Write Engine
try:
    write_engine = create_engine(
        db_settings.WRITE_DATABASE_URL,
        pool_size=db_settings.DATABASE_ENGINE_POOL_SIZE,
        max_overflow=db_settings.DATABASE_ENGINE_MAX_OVERFLOW,
        pool_pre_ping=db_settings.DATABASE_ENGINE_POOL_PING,
    )
except Exception as e:
    logger.error(f"Failed to connect to DB due to error: {e}")
    write_engine = None
finally:
    WriteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=write_engine)

# DB Read Only Engine
try:
    read_engine = create_engine(
        db_settings.READ_DATABASE_URL,
        pool_size=db_settings.DATABASE_ENGINE_POOL_SIZE,
        max_overflow=db_settings.DATABASE_ENGINE_MAX_OVERFLOW,
        pool_pre_ping=db_settings.DATABASE_ENGINE_POOL_PING,
    )
except Exception as e:
    logger.error(f"Failed to connect to DB due to error: {e}")
    read_engine = None
finally:
    ReadSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=read_engine)


if db_settings.ENABLE_DB_LOGGING == "true":

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(
        conn, cursor, statement, parameters, context, executemany
    ):
        """Before Query Execution Event."""
        query_id = str(uuid4())
        conn.info.setdefault("query_start_time", []).append(time.time())
        conn.info.setdefault("query_id", []).append(query_id)

        enable_query_start_log = False
        if enable_query_start_log:
            logger.debug(
                "TX: %s|Query Started: %s | Parameters: %s",
                query_id,
                statement.strip().replace("\n", ""),
                parameters,
            )

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        """After Query Execution Event."""
        total = time.time() - conn.info["query_start_time"].pop(-1)
        query_id = conn.info["query_id"].pop(-1)
        logger.debug(
            "TX: %s|Query Executed: %s | Parameters: %s | Total Time: %f",
            query_id,
            statement.strip().replace("\n", ""),
            parameters,
            total,
        )

# Dependency to get a write session
def get_write_session() -> Generator[Session, None, None]:
    """Dependency to get a write database session."""
    db = WriteSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency to get a read session
def get_read_session() -> Generator[Session, None, None]:
    """Dependency to get a read database session."""
    db = ReadSessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_session(session_type: str = "write") -> Generator[Session, None, None]:
    """
    Context manager for database session handling.

    Args:
        session_type (str): Type of session ("write" or "read").

    Yields:
        Generator[Session, None, None]: A database session.
    """
    if session_type == "write":
        session = WriteSessionLocal()
    elif session_type == "read":
        session = ReadSessionLocal()
    else:
        raise ValueError("Invalid session_type. Use 'write' or 'read'.")

    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# Aliases for write and read database sessions
WriteDbSession = Annotated[Session, Depends(get_write_session)]
ReadDbSession = Annotated[Session, Depends(get_read_session)]
