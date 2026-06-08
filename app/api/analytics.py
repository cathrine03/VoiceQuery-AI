from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy import func

from backend.app.db.session import SessionLocal
from backend.app.db.models.query_history import QueryHistory
from backend.app.db.models.user import User

from backend.app.auth.rbac import require_role
from fastapi import Depends

from backend.app.auth.rbac import (
    require_role
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/")
def get_analytics(
    user=Depends(require_role("admin"))
):
   


    db = SessionLocal()
    total_users = db.query(User).count()

    total_queries = db.query(
        QueryHistory
    ).count()

    avg_time = db.query(
        func.avg(
            QueryHistory.execution_time
        )
    ).scalar()

    total_rows = db.query(
        func.sum(
            QueryHistory.row_count
        )
    ).scalar()

    recent_queries = (
        db.query(QueryHistory)
        .order_by(
            QueryHistory.id.desc()
        )
        .limit(10)
        .all()
    )


    trend_data = (
        db.query(
            func.date(QueryHistory.created_at),
            func.count(QueryHistory.id)
        )
        .group_by(
            func.date(QueryHistory.created_at)
        )
        .all()
    )

    response_time_trend = (
        db.query(
            func.date(QueryHistory.created_at),
            func.avg(
                QueryHistory.execution_time
            )
        )
        .group_by(
            func.date(QueryHistory.created_at)
        )
        .all()
    )

    active_users = (
        db.query(
            QueryHistory.user_email,
            func.count(
                QueryHistory.id
            )
        )
        .group_by(
            QueryHistory.user_email
        )
        .order_by(
            func.count(
                QueryHistory.id
            ).desc()
        )
        .limit(5)
        .all()
    )

    top_questions = (
        db.query(
            QueryHistory.question,
            func.count(
                QueryHistory.id
            )
        )
        .group_by(
            QueryHistory.question
        )
        .order_by(
            func.count(
                QueryHistory.id
            ).desc()
        )
        .limit(5)
        .all()
    )

    recent_activity = (
        db.query(QueryHistory)
        .order_by(
            QueryHistory.created_at.desc()
        )
        .limit(10)
        .all()
    )
        
    db.close()
    
    return {
        "total_users": total_users,
        "total_queries": total_queries,
        "avg_time": round(
            avg_time or 0,
            2
        ),
        "total_rows": total_rows or 0,
        "success_rate": 100,

        "recent_activity": [
            {
                "email": q.user_email,
                "question": q.question,
                "execution_time": q.execution_time,
                "created_at": str(q.created_at)
            }
            for q in recent_activity
        ],

        "query_trend": [
            {
                "date": str(item[0]),
                "count": item[1]
            }
            for item in trend_data
        ],

        "response_time_trend": [
            {
                "date": str(item[0]),
                "avg_time": round(
                    item[1],
                    2
                )
            }
            for item in response_time_trend
        ],

        "recent_queries": [
            {
                "question": q.question,
                "execution_time": q.execution_time,
                "created_at": str(q.created_at)
            }
            for q in recent_queries
        ],

        "active_users": [
            {
                "email": item[0],
                "count": item[1]
            }
            for item in active_users
        ],

        "top_questions": [
            {
                "question": item[0],
                "count": item[1]
            }
            for item in top_questions
        ],

        
    }
