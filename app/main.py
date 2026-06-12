from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.analytics import (router as analytics_router)

from app.api.routes.auth import router as auth_router
from app.api.dashboard import (
    router as dashboard_router
)
from app.api.query import router as query_router
from app.api.history import router as history_router
from app.api.explain import (
    router as explain_router
)
from app.api.insights import router as insights_router

from app.routes.users import router as users_router
from app.routes.saved_queries import (
    router as saved_queries_router
)


app = FastAPI(
    title="VoiceQuery AI",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://voice-query-frontend.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
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
app.include_router(insights_router)
app.include_router(
    saved_queries_router
)

@app.get("/")
async def root():
    return {
        "message": "VoiceQuery AI Backend Running"
    }

@app.get("/cors-test")
def cors_test():
    return {"message": "cors works"}