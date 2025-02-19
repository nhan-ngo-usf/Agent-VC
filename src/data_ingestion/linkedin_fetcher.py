import requests
from typing import Dict, Optional
import logging
from src.models.linkedin_profile import LinkedInProfile

class LinkedInFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://nubela.co/proxycurl/api/v2"
        self.logger = logging.getLogger(__name__)
    
    def fetch_profile(self, linkedin_url: str) -> Optional[Dict]:
        """Fetch LinkedIn profile data using Proxycurl API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        endpoint = f"{self.base_url}/linkedin"
        params = {
            'url': linkedin_url,
            'use_cache': 'if-present'
        }
        
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error fetching LinkedIn profile for {linkedin_url}: {str(e)}")
            return None
    
    def process_profile_data(self, raw_data: Dict, startup_id: int) -> LinkedInProfile:
        """Process raw LinkedIn data into structured format"""
        profile = LinkedInProfile(
            startup_id=startup_id,
            raw_data=raw_data
        )
        
        # Extract basic info
        profile.full_name = raw_data.get('full_name')
        profile.headline = raw_data.get('headline')
        profile.summary = raw_data.get('summary')
        profile.country = raw_data.get('country')
        profile.city = raw_data.get('city')
        
        # Extract experiences
        profile.experiences = raw_data.get('experiences', [])
        
        # Extract education
        profile.education = raw_data.get('education', [])
        
        # Extract skills
        profile.skills = raw_data.get('skills', [])
        
        # Extract accomplishments
        profile.accomplishments = raw_data.get('accomplishments', [])
        
        # Extract network info
        profile.connections_count = raw_data.get('connections_count')
        
        return profile 