from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# sqlite file will be created automatically in this folder
DATABASE_URL = 'sqlite:///./books.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Provides a database session to each request, then closes it"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

