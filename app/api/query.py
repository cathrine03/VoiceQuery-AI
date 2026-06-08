from fastapi import APIRouter,Depends
import time

from app.services.sql_generator import generate_sql
from app.services.query_executor import execute_query
from app.services.sql_validator import validate_sql

from app.db.session import SessionLocal
from app.db.models.query_history import QueryHistory
from app.auth.dependencies import (
    get_current_user)

router = APIRouter(
    prefix="/query",
    tags=["Query"]
)



@router.post("/generate")
def generate_query(
    payload: dict,
    user=Depends(get_current_user)
):
    question = payload.get("question")

    total_start = time.time()

    # Generate SQL
    ai_start = time.time()

    sql = generate_sql(question)

    ai_end = time.time()

    # Validate SQL
    validate_sql(sql)

    # Execute SQL
    db_start = time.time()

    results = execute_query(sql)

    db_end = time.time()

    total_end = time.time()

    # Metrics
    ai_ms = round((ai_end - ai_start) * 1000, 2)
    db_ms = round((db_end - db_start) * 1000, 2)
    total_ms = round((total_end - total_start) * 1000, 2)

    row_count = len(results)

    # Save history
    db = SessionLocal()

    history = QueryHistory(
        question=question,
        sql=sql,
        row_count=row_count,
        execution_time=total_ms,
        user_email=user["sub"]
        
    )

    db.add(history)
    db.commit()
    db.close()

    return {
        "question": question,
        "sql": sql,
        "results": results,
        "row_count": row_count,
        "timings": {
            "ai_ms": ai_ms,
            "db_ms": db_ms,
            "total_ms": total_ms
        }
    }