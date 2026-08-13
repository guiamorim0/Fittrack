import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import Session, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session_local = Session(bind=engine)
Base = DeclarativeBase()