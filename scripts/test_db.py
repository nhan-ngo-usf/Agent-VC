import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import yaml
from src.database.db_manager import DatabaseManager
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def test_database():
    """Test database connection and setup"""
    try:
        # Load config
        config_path = project_root / "config" / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Initialize database manager
        db_manager = DatabaseManager(config["database"]["connection_string"])
        
        # Test connection
        if db_manager.check_connection():
            logger.info("Successfully connected to database")
            
            # Get table statistics
            stats = db_manager.get_table_stats()
            logger.info("Table statistics:")
            for table, count in stats.items():
                logger.info(f"{table}: {count} rows")
        else:
            logger.error("Failed to connect to database")
            
    except Exception as e:
        logger.error(f"Database test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_database() 