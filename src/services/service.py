from __future__ import annotations

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from src.models.base import Base

class SessionFactory:
    def __init__(self, username: str, password: str):
        self.DATABASE_URL = f"mysql+pymysql://{username}:{password}@127.0.0.1/marites"
        
        self.engine: Engine = create_engine(self.DATABASE_URL)
        self.Session: sessionmaker[Session] = sessionmaker(bind=self.engine)

        # Bind engine to Base
        Base.metadata.bind = self.engine

    def get_session(self) -> Session:
        """
        Function to get a session instance
        """
        return self.Session()