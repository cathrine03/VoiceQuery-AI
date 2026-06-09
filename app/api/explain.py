from fastapi import APIRouter, HTTPException
from app.services.sql_explainer import explain_sql

router = APIRouter(prefix="/explain", tags=["Explain"])


@router.post("/")
def explain(payload: dict):
    sql = payload.get("sql")

    if not sql or not sql.strip():
        raise HTTPException(
            status_code=400,
            detail="SQL is required"
        )

    explanation = explain_sql(sql)

    return {
        "explanation": explanation
    }