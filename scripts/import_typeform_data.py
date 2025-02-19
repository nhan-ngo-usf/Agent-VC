import os
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

import yaml
from src.database.db_manager import DatabaseManager
from src.data_ingestion.typeform_connector import TypeFormConnector
from src.utils.logger import setup_logger
from src.models.startup import Startup
from src.data_ingestion.linkedin_fetcher import LinkedInFetcher
from src.data_ingestion.website_crawler import WebsiteCrawler

logger = setup_logger(__name__)

def import_typeform_data():
    """Import data from Typeform and store in database"""
    try:
        # Load config
        config_path = project_root / "config" / "config.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        # Initialize connectors
        db_manager = DatabaseManager(config["database"]["connection_string"])
        typeform = TypeFormConnector(config["typeform"]["api_key"])
        linkedin_fetcher = LinkedInFetcher(config["proxycurl"]["api_key"])
        website_crawler = WebsiteCrawler()
        
        # Fetch responses
        responses = typeform.fetch_responses(config["typeform"]["form_id"])
        logger.info(f"Fetched {len(responses)} responses from Typeform")
        
        # Process and store each response
        with db_manager.session_scope() as session:
            for response in responses:
                try:
                    # Process startup data
                    startup = typeform.process_startup_data(response)
                    session.add(startup)
                    session.flush()  # Get startup ID
                    
                    # Fetch and process LinkedIn data if URL exists
                    if startup.linkedin_url:
                        linkedin_data = linkedin_fetcher.fetch_profile(startup.linkedin_url)
                        if linkedin_data:
                            profile = linkedin_fetcher.process_profile_data(
                                linkedin_data, 
                                startup.id
                            )
                            session.add(profile)
                            logger.info(f"Added LinkedIn profile for {startup.founder_name}")
                    
                    # Crawl website if URL exists
                    if startup.website:
                        website_data = website_crawler.process_website(
                            startup.website, 
                            startup.id
                        )
                        if website_data:
                            session.add(website_data)
                            logger.info(f"Added website data for {startup.company_name}")
                    
                    session.commit()
                    logger.info(f"Added submission {response['response_id']}")
                    
                except Exception as e:
                    logger.error(f"Error processing data: {str(e)}")
                    session.rollback()
                    continue
        
        logger.info("Import completed successfully")
        
    except Exception as e:
        logger.error(f"Import failed: {str(e)}")
        raise

if __name__ == "__main__":
    import_typeform_data() 