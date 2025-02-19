from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from src.database.db_manager import Base
from datetime import datetime

class WebsiteData(Base):
    __tablename__ = 'website_data'
    
    id = Column(Integer, primary_key=True)
    startup_id = Column(Integer, ForeignKey('startups.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Basic Info
    title = Column(String)
    description = Column(Text)
    
    # Content Analysis
    main_content = Column(Text)
    technologies = Column(JSON)  # Tech stack mentioned
    team_members = Column(JSON)  # Team information found
    contact_info = Column(JSON)  # Contact details
    social_links = Column(JSON)  # Social media links
    
    # SEO Data
    meta_tags = Column(JSON)
    og_tags = Column(JSON)
    
    # Raw Data
    raw_html = Column(Text)
    
    # Relationship
    startup = relationship("Startup", back_populates="website_data") 