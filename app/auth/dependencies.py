from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.jwt_handler import verify_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    print("AUTH HEADER RECEIVED")

    token = credentials.credentials

    print("TOKEN =", repr(token))

    try:
        payload = verify_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload

   