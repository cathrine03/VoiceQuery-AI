from fastapi import APIRouter, Depends

from backend.app.auth.rbac import (
    require_role
)

router = APIRouter(
    prefix="/test",
    tags=["Test"]
)

@router.get("/admin")
def admin_only(
    user=Depends(require_role("admin"))
):
    return {
        "message": "Admin access granted"
    }