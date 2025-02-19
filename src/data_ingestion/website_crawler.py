import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import logging
from urllib.parse import urljoin, urlparse
import re
from src.models.website_data import WebsiteData

class WebsiteCrawler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_website(self, url: str) -> Optional[str]:
        """Fetch website content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logger.error(f"Error fetching website {url}: {str(e)}")
            return None
    
    def extract_technologies(self, soup: BeautifulSoup) -> List[str]:
        """Extract technology stack information"""
        technologies = set()
        
        # Common technology keywords
        tech_keywords = [
            'react', 'angular', 'vue', 'python', 'django', 'flask',
            'node', 'aws', 'azure', 'gcp', 'kubernetes', 'docker',
            'tensorflow', 'pytorch', 'ai', 'ml', 'blockchain'
        ]
        
        # Search in text content
        text_content = soup.get_text().lower()
        for tech in tech_keywords:
            if tech in text_content:
                technologies.add(tech)
        
        # Search in meta tags and scripts
        for script in soup.find_all('script'):
            src = script.get('src', '')
            for tech in tech_keywords:
                if tech in src.lower():
                    technologies.add(tech)
        
        return list(technologies)
    
    def extract_team_members(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract team member information"""
        team_members = []
        
        # Look for common team section identifiers
        team_sections = soup.find_all(['div', 'section'], 
            class_=lambda x: x and ('team' in x.lower() or 'about' in x.lower()))
        
        for section in team_sections:
            # Look for person elements
            people = section.find_all(['div', 'article'], 
                class_=lambda x: x and ('person' in x.lower() or 'member' in x.lower()))
            
            for person in people:
                name = person.find(['h2', 'h3', 'h4'])
                title = person.find(['p', 'span'], 
                    class_=lambda x: x and ('title' in x.lower() or 'role' in x.lower()))
                
                if name:
                    team_members.append({
                        'name': name.text.strip(),
                        'title': title.text.strip() if title else None
                    })
        
        return team_members
    
    def extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information"""
        contact_info = {}
        
        # Extract email addresses
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, str(soup))
        if emails:
            contact_info['emails'] = list(set(emails))
        
        # Extract phone numbers
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, str(soup))
        if phones:
            contact_info['phones'] = list(set(phones))
        
        # Extract address
        address_section = soup.find(['div', 'section'], 
            class_=lambda x: x and 'address' in x.lower())
        if address_section:
            contact_info['address'] = address_section.text.strip()
        
        return contact_info
    
    def extract_social_links(self, soup: BeautifulSoup) -> Dict:
        """Extract social media links"""
        social_links = {}
        social_platforms = {
            'linkedin': r'linkedin\.com',
            'twitter': r'twitter\.com|x\.com',
            'facebook': r'facebook\.com',
            'instagram': r'instagram\.com',
            'github': r'github\.com'
        }
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            for platform, pattern in social_platforms.items():
                if re.search(pattern, href):
                    social_links[platform] = href
        
        return social_links
    
    def extract_meta_data(self, soup: BeautifulSoup) -> Dict:
        """Extract meta tags and OpenGraph data"""
        meta_data = {
            'meta_tags': {},
            'og_tags': {}
        }
        
        # Extract standard meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name')
            content = meta.get('content')
            if name and content:
                meta_data['meta_tags'][name] = content
        
        # Extract OpenGraph tags
        for meta in soup.find_all('meta', property=True):
            prop = meta.get('property')
            content = meta.get('content')
            if prop and content and prop.startswith('og:'):
                meta_data['og_tags'][prop] = content
        
        return meta_data
    
    def process_website(self, url: str, startup_id: int) -> Optional[WebsiteData]:
        """Process website and extract all relevant data"""
        html_content = self.fetch_website(url)
        if not html_content:
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Create website data object
            website_data = WebsiteData(
                startup_id=startup_id,
                raw_html=html_content
            )
            
            # Extract basic info
            website_data.title = soup.title.string if soup.title else None
            meta_description = soup.find('meta', {'name': 'description'})
            website_data.description = meta_description['content'] if meta_description else None
            
            # Extract main content (first significant text block)
            main_content = soup.find(['article', 'main', 'div'], 
                class_=lambda x: x and ('content' in x.lower() or 'main' in x.lower()))
            website_data.main_content = main_content.get_text() if main_content else None
            
            # Extract other data
            website_data.technologies = self.extract_technologies(soup)
            website_data.team_members = self.extract_team_members(soup)
            website_data.contact_info = self.extract_contact_info(soup)
            website_data.social_links = self.extract_social_links(soup)
            
            # Extract meta data
            meta_data = self.extract_meta_data(soup)
            website_data.meta_tags = meta_data['meta_tags']
            website_data.og_tags = meta_data['og_tags']
            
            return website_data
            
        except Exception as e:
            self.logger.error(f"Error processing website {url}: {str(e)}")
            return None 