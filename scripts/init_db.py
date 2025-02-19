import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import yaml
from src.database.db_manager import DatabaseManager
from src.models.startup import Startup
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def init_database():
    """Initialize the database with required tables"""
    try:
        # Load config
        config_path = project_root / "config" / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Initialize database manager
        db_manager = DatabaseManager(config["database"]["connection_string"])
        
        # Drop existing tables and create new ones
        db_manager.drop_db()
        db_manager.init_db()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

if __name__ == "__main__":
    init_database() 