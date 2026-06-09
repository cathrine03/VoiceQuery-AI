from fastapi import APIRouter, Depends, HTTPException
import traceback
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models.user import User


from app.auth.password import (
    hash_password,
    verify_password
)

from app.auth.jwt_handler import (
    create_access_token
)

from app.db.schemas.user import (
    UserCreate,
    UserLogin
)

from app.auth.dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/debug-env")
def debug():
    return {"db": DATABASE_URL}



@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()

        if existing_user:
            return {"error": "exists"}

        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role="user"
        )

        db.add(new_user)
        db.commit()

        return {"message": "User created successfully"}

    except Exception as e:
        print("🔥 REGISTER ERROR:", str(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user