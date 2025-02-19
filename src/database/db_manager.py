from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import List, Dict, Any
import logging

Base = declarative_base()

class DatabaseManager:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.logger = logging.getLogger(__name__)
    
    def init_db(self):
        """Initialize the database schema"""
        Base.metadata.create_all(self.engine)
    
    def drop_db(self):
        """Drop all tables - Use with caution!"""
        Base.metadata.drop_all(self.engine)
    
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()
    
    def check_connection(self) -> bool:
        """Test database connection"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            self.logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def get_table_stats(self) -> Dict[str, int]:
        """Get row counts for all tables"""
        stats = {}
        for table in Base.metadata.tables:
            with self.session_scope() as session:
                count = session.query(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                stats[table] = count
        return stats

