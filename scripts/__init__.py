import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import yaml
from src.database.db_manager import DatabaseManager
from src.models.startup import Startup
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def init_database():
    """Initialize the database with required tables"""
    # Load config
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    try:
        # Initialize database manager
        db_manager = DatabaseManager(config["database"]["connection_string"])
        
        # Create all tables
        db_manager.init_db()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

if __name__ == "__main__":
    init_database()