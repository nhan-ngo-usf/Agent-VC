from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.db_manager import Base
from datetime import datetime

class LinkedInProfile(Base):
    __tablename__ = 'linkedin_profiles'
    
    id = Column(Integer, primary_key=True)
    startup_id = Column(Integer, ForeignKey('startups.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Basic Info
    full_name = Column(String)
    headline = Column(String)
    summary = Column(String)
    country = Column(String)
    city = Column(String)
    
    # Experience and Education
    experiences = Column(JSON)  # Store full work history
    education = Column(JSON)    # Store education history
    
    # Skills and Accomplishments
    skills = Column(JSON)
    accomplishments = Column(JSON)
    
    # Network Info
    connections_count = Column(Integer)
    
    # Raw Data
    raw_data = Column(JSON)  # Store complete raw response
    
    # Relationship
    startup = relationship("Startup", back_populates="linkedin_profile") 