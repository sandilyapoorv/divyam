from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.database import engine, Base, SessionLocal
from backend.app.data.seeds.mospi_data import seed_database
from backend.app.api.auth import router as auth_router
from backend.app.api.competencies import router as comp_router
from backend.app.api.igot import router as igot_router
from backend.app.api.documents import router as doc_router
from backend.app.api.quizzes import router as quiz_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed initial data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(comp_router, prefix=settings.API_V1_STR)
app.include_router(igot_router, prefix=settings.API_V1_STR)
app.include_router(doc_router, prefix=settings.API_V1_STR)
app.include_router(quiz_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "cadre_scope": "MoSPI / ISS / SSS / State DES"
    }

@app.get("/")
def root():
    return {
        "message": "Welcome to DRIVYAM Official Statistical Learning Platform API",
        "docs_url": "/docs",
        "health_url": "/health"
    }
