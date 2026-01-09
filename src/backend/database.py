import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import QueuePool

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent / ".env.backend"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv() # Fallback to .env

# Database URL should be in .env: 
# DATABASE_URL=postgresql://user:pass@ep-hostname.region.aws.neon.tech/dbname?sslmode=require
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback for local development if Neon URL is not provided
    DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    poolclass=QueuePool,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
