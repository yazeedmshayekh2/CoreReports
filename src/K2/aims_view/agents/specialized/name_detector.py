"""
Name Detection Agent for identifying names in user queries
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class NameDetector:
    """Name detection agent for identifying and classifying names"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create name detection agent"""
        return Agent(
            role="Name Detection Specialist",
            goal="Detect and classify names in user questions as customer, agent/broker, or user names",
            backstory="""You are an expert in analyzing natural language text to identify and classify 
            names mentioned in insurance-related questions. You can distinguish between customer names, 
            agent/broker names, and user references with high accuracy.
            
            Your expertise includes:
            - Recognizing personal names in various formats (first last, full names, nicknames)
            - Distinguishing between customer names and agent/broker names based on context
            - Understanding question patterns that reference customers vs agents/brokers
            - Extracting names accurately from complex sentences
            - Understanding that AGENT and BROKER are the same thing
            
            Classification Guidelines:
            - CUSTOMER: Names mentioned in context of "find customer", "customer X", "policies for John", etc.
            - AGENT: Names in context of "agent Y", "broker Z", "sold by", "written by", etc. 
                     NOTE: AGENT and BROKER are the SAME THING - treat them identically
            - USER: Names referring to system users (stored in DOC_USER_NO, DOC_USER_NAME columns)
            - NONE: No names detected in the question
            
            You analyze the semantic context to make accurate classifications.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_llm(),
            max_iter=2
        )
    
    def get_agent(self) -> Agent:
        """Get the name detector agent"""
        return self.agent
