# setting path
import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager


from app.core.config import POSTGRESQL


sync_engine = create_engine(f'postgresql+psycopg2://{POSTGRESQL.get("user")}:{POSTGRESQL.get("password")}@{POSTGRESQL.get("host")}/{POSTGRESQL.get("database")}?',
                            pool_size=5, # макс подключений
                            max_overflow=10, # Доп подключения
                            echo=POSTGRESQL.get("echo"),
                            )

MySession = sessionmaker(bind=sync_engine)
