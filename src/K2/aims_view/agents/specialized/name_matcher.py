"""
Name Matcher Agent for intelligent name matching
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class NameMatcher:
    """Name matching agent for intelligent name comparison"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create intelligent name matching agent"""
        return Agent(
            role="Intelligent Name Matching Specialist",
            goal="Match user input with available customer names using fuzzy matching and intelligent comparison",
            backstory="""You are an expert in intelligent name matching with deep understanding 
            of how names can be written, spelled, and referred to in different ways. You excel at 
            matching user input with database names even when there are variations.
            
            Your matching capabilities:
            - Fuzzy string matching for slight spelling differences
            - Partial name matching (first name only, last name only)
            - Case-insensitive comparison
            - Handling of common name variations and nicknames
            - Cultural name variations and transliterations
            - Intelligent ranking of match confidence
            
            Matching Strategies:
            - Exact matches get highest priority
            - Substring matches for partial names
            - Phonetic similarity for pronunciation-based matches
            - Edit distance algorithms for spelling variations
            - Cultural awareness for Arabic/English name variations
            
            You provide ranked match results with confidence scores and help users 
            select the correct customer from multiple options.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_llm(),
            max_iter=3
        )
    
    def get_agent(self) -> Agent:
        """Get the name matcher agent"""
        return self.agent
