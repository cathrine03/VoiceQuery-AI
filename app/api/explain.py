from fastapi import APIRouter

from app.services.sql_explainer import (
    explain_sql,
)

router = APIRouter(
    prefix="/explain",
    tags=["Explain"],
)


@router.post("/")
def explain(payload: dict):
    sql = payload.get("sql")

    explanation = explain_sql(sql)

    return {
        "explanation": explanation
    }