from fastapi import APIRouter, Depends, HTTPException
from app.auth.dependencies import (
    get_current_user
)

from app.db.session import SessionLocal
from app.db.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        return {
            "detail": "Forbidden"
        }

    db = SessionLocal()

    users = (
        db.query(User)
        .order_by(User.id)
        .all()
    )

    result = []

    for u in users:
        result.append(
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "role": u.role,
            }
        )

    db.close()

    return result


@router.put("/{user_id}/role")
def update_role(
    user_id: int,
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    db = SessionLocal()

    target_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    
    if not target_user:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if target_user.email == user["sub"]:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Cannot change your own role"
        )

    if target_user.role == "admin":
        target_user.role = "user"
    else:
        target_user.role = "admin"

    db.commit()

    result = {
        "message": "Role updated",
        "role": target_user.role
    }

    db.close()

    return result


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user=Depends(get_current_user)
):
    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    db = SessionLocal()

    target_user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not target_user:
        db.close()

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if target_user.email == user["sub"]:
        db.close()

        raise HTTPException(
            status_code=400,
            detail="Cannot delete yourself"
        )

    db.delete(target_user)

    db.commit()

    db.close()

    return {
        "message": "User deleted"
    }