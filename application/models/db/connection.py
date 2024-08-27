import os
import random

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if os.getenv("PYTHON_ENV") == "TEST":
    DATABASE_URL = f"sqlite:///test-{random.randint(10000, 99999)}.db"
else:
    DATABASE_URL = "sqlite:///main.db"

engine = create_engine(DATABASE_URL, echo=False)

# 세션 생성
session = sessionmaker(bind=engine)()

# Base 클래스 생성
Base = declarative_base()
