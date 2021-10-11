from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

__HEROKU_POSTGRES_PREFIX = "postgres://"
__SQL_ALCHEMY_POSTGRES_PREFIX_NEEDED = "postgresql://"

DATABASE_URL = settings.DATABASE_URL;

if __HEROKU_POSTGRES_PREFIX in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(__HEROKU_POSTGRES_PREFIX, __SQL_ALCHEMY_POSTGRES_PREFIX_NEEDED, 1)

engine = create_engine(
    DATABASE_URL,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
