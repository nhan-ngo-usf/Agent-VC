import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.data_ingestion.website_crawler import WebsiteCrawler
from src.models.startup import Startup
from src.models.website_data import WebsiteData
from src.database.db_manager import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml

def load_config():
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)

def test_crawl_existing_websites():
    # Load configuration
    config = load_config()
    
    # Setup database connection
    engine = create_engine(config["database"]["connection_string"])
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Initialize crawler
    crawler = WebsiteCrawler()
    
    try:
        # Get all startups with websites
        startups = session.query(Startup).filter(
            Startup.website.isnot(None)
        ).all()
        
        print(f"Found {len(startups)} websites to crawl")
        
        # Test crawling each website
        for startup in startups:
            print(f"\nTesting website for startup {startup.id}: {startup.website}")
            
            try:
                website_data = crawler.process_website(startup.website, startup.id)
                
                if website_data:
                    print("✓ Successfully crawled website")
                    print(f"  - Title: {website_data.title}")
                    print(f"  - Technologies found: {website_data.technologies}")
                    print(f"  - Team members found: {len(website_data.team_members)}")
                    print(f"  - Social links found: {list(website_data.social_links.keys())}")
                    
                    # Optionally save the results
                    # session.add(website_data)
                    # session.commit()
                else:
                    print("✗ Failed to crawl website")
            
            except Exception as e:
                print(f"✗ Error processing {startup.website}: {str(e)}")
                continue
            
    finally:
        session.close()

if __name__ == "__main__":
    test_crawl_existing_websites() 