from fastapi import APIRouter, Depends

from backend.app.db.session import SessionLocal
from backend.app.db.models.query_history import QueryHistory

from backend.app.auth.dependencies import (
    get_current_user
)

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/")
def get_history(
    user=Depends(get_current_user)
):
    db = SessionLocal()

    email = user["sub"]

    history = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.user_email == email
        )
        .order_by(
            QueryHistory.id.desc()
        )
        .all()
    )

    result = []

    for item in history:
        result.append({
            "id": item.id,
            "question": item.question,
            "sql": item.sql,
            "row_count": item.row_count,
            "execution_time": item.execution_time,
            "created_at": str(item.created_at)
        })

    db.close()

    return result