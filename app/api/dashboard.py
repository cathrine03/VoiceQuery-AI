from fastapi import APIRouter, Depends
from sqlalchemy import func
from datetime import datetime, timedelta

from app.auth.dependencies import (
    get_current_user
)

from app.db.session import SessionLocal
from app.db.models.query_history import QueryHistory
from app.db.models.saved_query import SavedQuery

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    user=Depends(get_current_user)
):
    db = SessionLocal()

    email = user["sub"]

    total_queries = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.user_email == email
        )
        .count()
    )

    avg_time = (
        db.query(
            func.avg(
                QueryHistory.execution_time
            )
        )
        .filter(
            QueryHistory.user_email == email
        )
        .scalar()
    )

    total_rows = (
        db.query(
            func.sum(
                QueryHistory.row_count
            )
        )
        .filter(
            QueryHistory.user_email == email
        )
        .scalar()
    )

    last_query = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.user_email == email
        )
        .order_by(
            QueryHistory.id.desc()
        )
        .first()
    )

    avg_rows = (
        db.query(
            func.avg(
                QueryHistory.row_count
            )
        )
        .filter(
            QueryHistory.user_email == email
        )
        .scalar()
    )


    most_used_query = (
        db.query(
            QueryHistory.question,
            func.count(
                QueryHistory.id
            ).label("count")
        )
        .filter(
            QueryHistory.user_email == email
        )
        .group_by(
            QueryHistory.question
        )
        .order_by(
            func.count(
                QueryHistory.id
            ).desc()
        )
        .first()
    )


    week_ago = (
        datetime.utcnow()
        - timedelta(days=7)
    )

    queries_this_week = (
        db.query(
            QueryHistory
        )
        .filter(
            QueryHistory.user_email == email,
            QueryHistory.created_at >= week_ago
        )
        .count()
    )

    saved_count = (
        db.query(
            SavedQuery
        )
        .filter(
            SavedQuery.user_email == email
        )
        .count()
    )

    trend_data = (
        db.query(
            func.date(QueryHistory.created_at),
            func.count(QueryHistory.id)
        )
        .filter(
            QueryHistory.user_email == email
        )
        .group_by(
            func.date(QueryHistory.created_at)
        )
        .order_by(
            func.date(QueryHistory.created_at)
        )
        .all()
    )

    top_questions = (
        db.query(
            QueryHistory.question,
            func.count(
                QueryHistory.id
            )
        )
        .filter(
            QueryHistory.user_email == email
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
    
    recent_queries = (
        db.query(QueryHistory)
        .filter(
            QueryHistory.user_email == email
        )
        .order_by(
            QueryHistory.id.desc()
        )
        .limit(5)
        .all()
    )

    db.close()

    return {
        "total_queries": total_queries,

        "avg_time": round(
            avg_time or 0,
            2
        ),

        "total_rows": total_rows or 0,

        "last_query_time":
            str(last_query.created_at)
            if last_query
            else None,

        "avg_rows": round(
            avg_rows or 0,
            2
        ),

        "saved_queries":
            saved_count,

        "queries_this_week":
            queries_this_week,

        "most_used_query":
            most_used_query.question
            if most_used_query
            else "N/A",

        "query_trend": [
            {
                "date": str(item[0]),
                "count": item[1]
            }
            for item in trend_data
        ],

        "top_questions": [
            {
                "question": item[0],
                "count": item[1]
            }
            for item in top_questions
        ],

        "recent_queries": [
            {
                "question": q.question,
                "execution_time": q.execution_time,
                "created_at": str(q.created_at)
            }
            for q in recent_queries
        ]
    }