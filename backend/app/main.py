from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from sqlalchemy import text
from app.db.session import engine

app = FastAPI(
    title="FastAPI Template",
    description="A template for FastAPI applications.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1", tags=["v1"])


@app.on_event("startup")
def startup():
    print("Starting up...")


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
        **({"db_error": db_error} if db_error else {})
    }
