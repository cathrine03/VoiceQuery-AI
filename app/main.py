from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.analytics import (router as analytics_router)

from backend.app.api.routes.auth import router as auth_router
from backend.app.api.dashboard import (
    router as dashboard_router
)
from backend.app.api.query import router as query_router
from backend.app.api.history import router as history_router
from backend.app.api.explain import (
    router as explain_router
)
from test import (
    router as test_router
)
from backend.app.routes.users import router as users_router
from backend.app.routes.saved_queries import (
    router as saved_queries_router
)


app = FastAPI(
    title="VoiceQuery AI",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(
    dashboard_router
)
app.include_router(query_router)
app.include_router(history_router)
app.include_router(analytics_router)
app.include_router(explain_router)
app.include_router(test_router)
app.include_router(
    saved_queries_router
)

@app.get("/")
async def root():
    return {
        "message": "VoiceQuery AI Backend Running"
    }