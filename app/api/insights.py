from fastapi import APIRouter
from app.services.ai_insights import generate_insights

router = APIRouter(prefix="/insights", tags=["AI Insights"])


@router.post("/")
def get_insights(payload: dict):
    return {
        "insights": generate_insights(
            payload["question"],
            payload["sql"],
            payload["results"]
        )
    }