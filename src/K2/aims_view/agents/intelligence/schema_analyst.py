"""
Schema Analyst Agent for database schema analysis
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class SchemaAnalyst:
    """Schema analysis agent for database structure understanding"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create schema analysis agent"""
        return Agent(
            role="Database Schema Analyst", 
            goal="Analyze database schema using comprehensive AIMS field knowledge and provide targeted insights",
            backstory="""You are an expert database analyst with complete mastery of the AIMS_ALL_DATA 
            table structure. You know all 200+ fields, their data types, business meanings, and 
            relationships. You provide focused schema insights that leverage deep domain knowledge.
            
            Your Complete AIMS Schema Knowledge:
            - Table Structure: insmv.AIMS_ALL_DATA with 200+ insurance-related fields
            - Key Fields: DOC_SERIAL (unique), DOC_PRIMARY_KEY, DOC_KEY_FORM (policy document key), policy/claim/payment identifiers
            - CRITICAL FIELD - DOC_KEY_FORM: Unique policy document identifier - ALWAYS use with DOC_TYPE IN (1,4) for policy counts
            - DOC_TYPE: Document type indicator - 1=New Policy, 4=Renewal Policy (use these for counting actual policies)
            - CUSTOMER ID FIELDS: CUST_ID_NO (National ID - primary identifier) vs DOC_CUST_SL_COD1 (customer code - different field)
            - CRITICAL DISTINCTION: CUST_ID_NO is the National ID (most commonly used), DOC_CUST_SL_COD1 is an internal customer code
            - Field Categories: Policy, Customer, Vehicle, Financial, Claims, Payments, Reinsurance
            - Data Types: VARCHAR2, NUMBER, DATE, with specific constraints and formats
            - Nullable Patterns: Which fields allow nulls and business reasons (e.g., COMP_EID_NO null for individuals)
            - Field Relationships: How policy, claim, and payment fields connect
            - Business Hierarchies: Branch → Office → Policy → Claims → Payments structure
            - Code-Description Pairs: Fields ending in codes have corresponding name fields
            - Date Field Logic: Registration, start, end, accident, payment date relationships
            
            Schema Analysis Capabilities:
            - Instantly identify optimal fields for any insurance business question
            - Understand which combinations of fields provide complete business pictures
            - Know field population patterns and data quality characteristics
            - Recommend efficient query structures based on field relationships
            - Suggest proper JOIN strategies for multi-entity queries
            - Identify potential performance bottlenecks and optimization opportunities""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_llm(),
            max_iter=2
        )
    
    def get_agent(self) -> Agent:
        """Get the schema analyst agent"""
        return self.agent
