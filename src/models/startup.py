from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from src.database.db_manager import Base
from datetime import datetime

class Startup(Base):
    __tablename__ = 'startups'
    
    id = Column(Integer, primary_key=True)
    submission_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Founder Info
    founder_name = Column(String)
    founder_title = Column(String)
    founder_email = Column(String)
    founder_phone = Column(String)
    linkedin_url = Column(String)
    founder_experience = Column(String)
    
    # Company Info
    company_name = Column(String)
    website = Column(String)
    description = Column(String)
    location = Column(String)
    legal_structure = Column(String)
    problem_statement = Column(String)
    solution_statement = Column(String)
    unique_value = Column(String)
    customer_validation = Column(String)
    
    # Metrics (updated types)
    active_users = Column(Integer)
    paying_users = Column(Integer)
    customer_count = Column(Integer)
    mrr = Column(Float)
    
    # Funding Info (updated types)
    funding_stage = Column(String)
    round_size = Column(Float)
    valuation = Column(Float)
    commitments = Column(Float)
    lead_investor = Column(String)
    
    # Additional Info
    pitch_deck_url = Column(String)
    referral_source = Column(String)
    
    # Raw Data
    raw_typeform_data = Column(JSON)

    # Add the relationship
    linkedin_profile = relationship("LinkedInProfile", back_populates="startup", uselist=False)
    website_data = relationship("WebsiteData", back_populates="startup", uselist=False)
