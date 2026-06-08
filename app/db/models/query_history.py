from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    Float,
    DateTime
)

from sqlalchemy.sql import func

from app.db.base import Base


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    sql = Column(
        Text,
        nullable=False
    )

    row_count = Column(
        Integer,
        nullable=False
    )

    execution_time = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user_email = Column(
    String,
    nullable=True
)