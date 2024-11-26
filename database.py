from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# POSTGRES_USER = "postgres"
# POSTGRES_PASSWORD = "n1m010"
# POSTGRES_DB = "soft"
# POSTGRES_HOST = "localhost"
# POSTGRES_PORT = "5432"


POSTGRES_USER = "rasberry"
POSTGRES_PASSWORD = "123456"
POSTGRES_DB = "soft"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
