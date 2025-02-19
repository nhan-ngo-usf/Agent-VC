import logging
import yaml
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """Set up and return a logger instance"""
    
    # Load config
    config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(config["logging"]["level"])
    
    # Create handler
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(config["logging"]["format"])
    )
    
    logger.addHandler(handler)
    return logger
