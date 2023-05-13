from app.core.models.database import Base
import app.database as _database


def create_database():
    try:
        Base.metadata.create_all(bind=_database.engine)
    except Exception as e:
        print(f"Error while creating tables: {e}")


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

