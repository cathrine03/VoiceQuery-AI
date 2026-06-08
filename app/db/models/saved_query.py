from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from datetime import datetime

from backend.app.db.base import Base


class SavedQuery(Base):
    __tablename__ = "saved_queries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_email = Column(
        String,
        nullable=False
    )

    question = Column(
        String,
        nullable=False
    )



    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )