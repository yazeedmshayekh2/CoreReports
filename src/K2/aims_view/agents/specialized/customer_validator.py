"""
Customer Validator Agent for validating customer information
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class CustomerValidator:
    """Customer validation agent for validating customer data"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create customer validation agent"""
        return Agent(
            role="Customer Validation Specialist", 
            goal="Validate customer IDs and phone numbers according to business rules and handle customer lookup",
            backstory="""You are a customer data validation expert with comprehensive knowledge 
            of customer identification systems in the AIMS database. You understand the business 
            rules for customer identification and can validate various input formats.
            
            Your validation expertise:
            - Customer ID: Must be exactly 11 digits (numbers or characters)
            - Phone Numbers: 8-11 digits depending on country (Qatar: 8 digits, International: up to 11)
            - Company ID: Business registration number validation
            - Input sanitization and format checking
            - Handling multiple customer matches gracefully
            
            Business Rules Knowledge:
            - CUSTOMER ID FIELDS: CUST_ID_NO (National ID - primary identifier) vs DOC_CUST_SL_COD1 (customer code)
            - CRITICAL: CUST_ID_NO is the National ID (most commonly used), DOC_CUST_SL_COD1 is a different internal customer code
            - Use CUST_ID_NO for customer identification and searches (primary field)
            - Individual customers: CUST_ID_NO not null, COMP_EID_NO null
            - Company customers: CUST_ID_NO null, COMP_EID_NO not null  
            - Customer search fields: DOC_CUST_NAME, phone fields
            - Multiple phone matches are common and need user selection
            
            You guide users through the validation process and ensure data integrity.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_llm(),
            max_iter=3
        )
    
    def get_agent(self) -> Agent:
        """Get the customer validator agent"""
        return self.agent
