from __future__ import annotations

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from src.models.base import Base

class SessionFactory:
    def __init__(self, username: str, password: str):
        try:
            self.DATABASE_URL = f"mysql+pymysql://{username}:{password}@127.0.0.1/marites"
            
            self.engine: Engine = create_engine(self.DATABASE_URL)
            self.session: sessionmaker[Session] = sessionmaker(bind=self.engine)
            self.Session = self.session()
            
            # Bind engine to Base
            Base.metadata.bind = self.engine
        
        except Exception as err:
            print(err)
            quit()

    def get_session(self) -> Session:
        """
        Function to get a session instance
        """
        try:
            self.Session.connection()
        
        except OperationalError as err:
            raise err
        
        else:
            return self.Session