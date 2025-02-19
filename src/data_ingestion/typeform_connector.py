from typing import Dict, List, Union
import requests
from src.models.startup import Startup
from src.utils.logger import setup_logger
import re
import logging

logger = setup_logger(__name__)

class TypeFormConnector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.typeform.com/forms"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.logger = logging.getLogger(__name__)
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Remove all non-numeric characters except +
        cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
        return len(cleaned) >= 10 and len(cleaned) <= 15
    
    def _normalize_number(self, value: str, as_float: bool = False) -> Union[int, float, None]:
        """Convert string numbers (e.g., '30,000') to numeric types"""
        if not value:
            return None
            
        try:
            # Remove currency symbols, commas, and spaces
            cleaned = ''.join(c for c in value if c.isdigit() or c == '.')
            if as_float:
                return float(cleaned)
            return int(float(cleaned))  # handle cases like "1.0"
        except (ValueError, TypeError):
            self.logger.warning(f"Could not convert value '{value}' to number")
            return None
    
    def process_startup_data(self, response: Dict) -> Startup:
        """Process and validate a single Typeform response"""
        startup = Startup(
            submission_id=response["response_id"],
            raw_typeform_data=response
        )
        
        answers = {
            answer["field"]["ref"]: answer 
            for answer in response["answers"]
        }
        
        # Field mappings with actual Typeform field refs
        field_mappings = {
            "aea1a8b5-3439-418c-b873-5602a2b6107e": "founder_name",
            "48820fb6-e43c-4e5c-8f9c-d74428f9a679": "founder_title",
            "1c0f2be0-a322-4da4-8007-5dd5fb6d48d6": "founder_email",
            "39d91d37-55d8-4817-9454-84d663b31ae8": "founder_phone",
            "fb9e9315-f726-4642-aa37-448f5a7f5d7f": "linkedin_url",
            "3ad66bfa-4df3-4067-9f7c-0b5037459579": "company_name",
            "2abac0ae-4a29-4276-8f72-7a045fac3f01": "website",
            "ed20ab50-f510-4b63-bbde-8b08b7e856e8": "description",
            "de0b82e4-9ef5-484d-aa7d-2361d409f2ab": "location",
            "c2cf1c53-f317-4bc3-91cc-ef0e31d93cec": "legal_structure",
            "548fd3a6-97c7-44ab-9548-46511dc92d19": "problem_statement",
            "ce96d524-7fde-4e74-95d1-9a0985c862ab": "solution_statement",
            "7bd2bd0f-cb0b-4ba2-b995-b0efec6a12cd": "unique_value",
            "8554e2ef-2e62-4cec-99b0-70aebe2965c1": "customer_validation",
            "6a107f69-c163-442e-a085-50e115b9904c": "active_users",
            "a3859307-8e1b-4cc5-8115-79bdd2652f77": "paying_users",
            "5fc2054e-be02-467b-b498-2b9b890cc35a": "customer_count",
            "10b68790-547f-4e9a-9fd2-4988bbef853e": "mrr",
            "2bd5e597-a398-4302-9af5-8d4ba1d3fe8c": "funding_stage",
            "e355201f-7fda-4218-bbba-0b6ac2b8295f": "round_size",
            "0f73410a-5e35-47d2-a19e-3f13832eb499": "valuation",
            "d39d8d40-0326-4783-84e2-5348818157ce": "commitments",
            "bcb24889-41fe-430d-a340-fb051f315458": "lead_investor",
            "6610cdd2-4fe3-4bd0-a5a3-58591e9e5e15": "pitch_deck_url",
            "be3ac46f-70dd-49bf-b5b5-32667ed1b2a4": "referral_source",
            "246a0303-c6f7-4d57-8907-021bcf43c641": "founder_experience"
        }
        
        # Process each field with validation and normalization
        for ref, answer in answers.items():
            value = self._get_answer_value(answer)
            
            # Email validation
            if ref == "1c0f2be0-a322-4da4-8007-5dd5fb6d48d6":  # email field
                if not self._validate_email(value):
                    self.logger.error(f"Invalid email format: {value}")
                    continue
                startup.founder_email = value
            
            # Phone validation
            elif ref == "39d91d37-55d8-4817-9454-84d663b31ae8":  # phone field
                if not self._validate_phone(value):
                    self.logger.error(f"Invalid phone format: {value}")
                    continue
                startup.founder_phone = value
            
            # Integer fields
            elif ref in ["6a107f69-c163-442e-a085-50e115b9904c",  # active_users
                        "a3859307-8e1b-4cc5-8115-79bdd2652f77",  # paying_users
                        "5fc2054e-be02-467b-b498-2b9b890cc35a"]: # customer_count
                normalized = self._normalize_number(value, as_float=False)
                if normalized is not None:
                    setattr(startup, field_mappings[ref], normalized)
            
            # Float fields
            elif ref in ["10b68790-547f-4e9a-9fd2-4988bbef853e",  # mrr
                        "e355201f-7fda-4218-bbba-0b6ac2b8295f",  # round_size
                        "0f73410a-5e35-47d2-a19e-3f13832eb499",  # valuation
                        "d39d8d40-0326-4783-84e2-5348818157ce"]: # commitments
                normalized = self._normalize_number(value, as_float=True)
                if normalized is not None:
                    setattr(startup, field_mappings[ref], normalized)
            
            # Other fields
            else:
                field_name = field_mappings.get(ref)
                if field_name:
                    setattr(startup, field_name, value)
        
        return startup
    
    def _get_answer_value(self, answer: Dict) -> any:
        """Extract the value from a Typeform answer based on its type"""
        if "text" in answer:
            return answer["text"]
        elif "number" in answer:
            return answer["number"]
        elif "choice" in answer:
            return answer["choice"]["label"]
        elif "choices" in answer:
            return answer["choices"]["labels"]
        elif "email" in answer:
            return answer["email"]
        elif "url" in answer:
            return answer["url"]
        elif "phone_number" in answer:
            return answer["phone_number"]
        return None

    def _clean_number(self, value: str) -> float:
        """Clean and convert number strings to float"""
        if not value:
            return 0.0
        # Remove currency symbols, commas, and spaces
        cleaned = ''.join(c for c in value if c.isdigit() or c == '.')
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def fetch_responses(self, form_id: str) -> List[Dict]:
        """Fetch responses from a specific TypeForm"""
        endpoint = f"{self.base_url}/{form_id}/responses"
        
        params = {
            "page_size": 100,  # Maximum allowed by Typeform
            "completed": True  # Only get completed responses
        }
        
        response = requests.get(endpoint, headers=self.headers, params=params)
        response.raise_for_status()
        
        return response.json()["items"]
