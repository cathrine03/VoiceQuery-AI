from fastapi import APIRouter, Depends, HTTPException
from backend.app.auth.dependencies import get_current_user
from backend.app.db.session import SessionLocal
from backend.app.db.models.saved_query import SavedQuery

router = APIRouter(prefix="/saved-queries", tags=["Saved Queries"])

@router.post("/")
def save_query(
    data: dict,
    user=Depends(get_current_user)
):
    db = SessionLocal()

    existing = (
        db.query(SavedQuery)
        .filter(
            SavedQuery.user_email == user["sub"],
            SavedQuery.question == data["question"]
        )
        .first()
    )

    if existing:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Already saved"
        )

    saved = SavedQuery(
        user_email=user["sub"],
        question=data["question"],
    )

    db.add(saved)
    db.commit()
    db.close()

    return {"message": "Saved"}

@router.get("/")
def get_saved(user=Depends(get_current_user)):
    db = SessionLocal()

    queries = (
        db.query(SavedQuery)
        .filter(SavedQuery.user_email == user["sub"])
        .order_by(SavedQuery.id.desc())
        .all()
    )

    db.close()

    return [
        {
            "id": q.id,
            "question": q.question,
            "created_at": str(q.created_at)
        }
        for q in queries
    ]


@router.delete("/{query_id}")
def delete_saved(query_id: int, user=Depends(get_current_user)):
    db = SessionLocal()

    query = (
        db.query(SavedQuery)
        .filter(
            SavedQuery.id == query_id,
            SavedQuery.user_email == user["sub"]
        )
        .first()
    )

    if not query:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Not found"
        )

    db.delete(query)
    db.commit()
    db.close()

    return {"message": "Deleted"}