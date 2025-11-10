from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Example SQLite in-memory DB
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    """Provide a transactional scope for database operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()