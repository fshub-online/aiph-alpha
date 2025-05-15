from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


db_url = settings.database_url
engine_args = {}

engine = create_engine(db_url, **engine_args)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
