from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.api import api_router
from sqlalchemy import text
from app.db.session import engine
from app.core.config import settings
import sys

app = FastAPI(
    title="FastAPI Template",
    description="A template for FastAPI applications.",
    version="0.1.0",
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=["*"],
#   allow_credentials=True,
#   allow_methods=["*"],
#   allow_headers=["*"],
# )

app.include_router(api_router, prefix="/api/v1", tags=["v1"])


@app.on_event("startup")
def startup():
    print("Starting up...", file=sys.stdout, flush=True)
    print("Loaded settings:", file=sys.stdout, flush=True)
    for key, value in settings.__dict__.items():
        if not key.startswith("_"):
            print(f"   {key}: {value}", file=sys.stdout, flush=True)
    print("Database URL:", settings.database_url, file=sys.stdout, flush=True)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection: OK", file=sys.stdout, flush=True)
    except Exception as e:
        print(f"Database connection: FAILED - {e}", file=sys.stdout, flush=True)


@app.on_event("shutdown")
def shutdown():
    print("Shutting down...")


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Template!"}


@app.get("/health")
async def health():
    db_status = "unknown"
    db_error = None
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = "unhealthy"
        db_error = str(e)
    return {
        "status": "healthy",
        "database": db_status,
        **({"db_error": db_error} if db_error else {}),
    }
