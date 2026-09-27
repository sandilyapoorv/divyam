import pytest
from sqlalchemy import text

def test_settings_load():
    from backend.app.core.config import settings
    assert settings.PROJECT_NAME == "DRIVYAM"
    assert "sqlite" in settings.DATABASE_URL or "postgresql" in settings.DATABASE_URL
    assert settings.API_V1_STR == "/api"

def test_database_connection():
    from backend.app.core.database import SessionLocal, engine, Base
    assert engine is not None
    assert Base is not None
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT 1")).scalar()
        assert result == 1
    finally:
        db.close()
