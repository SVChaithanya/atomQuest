from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("database is not connected")
engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db

    finally:
        db.close()
     


