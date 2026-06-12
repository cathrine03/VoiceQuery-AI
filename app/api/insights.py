from fastapi import APIRouter, HTTPException
from app.services.ai_insights import generate_insights

router = APIRouter(prefix="/insights", tags=["AI Insights"])


@router.post("/")
def get_insights(payload: dict):

    question = payload.get("question")
    sql = payload.get("sql")
    results = payload.get("results", [])

    if not question or not sql:
        raise HTTPException(status_code=400, detail="Missing question or sql")

    try:
        return {
            "insights": generate_insights(question, sql, results)
        }

    except Exception as e:
        print("INSIGHTS ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))