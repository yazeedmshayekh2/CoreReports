"""
Execution Specialist Agent for query execution
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class ExecutionSpecialist:
    """Query execution specialist for safe query execution"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create query execution specialist"""
        return Agent(
            role="Query Execution Specialist",
            goal="Execute queries safely and handle all execution scenarios including errors and optimizations",
            backstory="""You are responsible for the reliable execution of SQL queries. You handle 
            error scenarios gracefully, can suggest query modifications when needed, and understand 
            how to interpret Oracle error messages to provide actionable feedback. You ensure all 
            queries execute safely within security constraints.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_llm(),
            max_iter=2
        )
    
    def get_agent(self) -> Agent:
        """Get the execution specialist agent"""
        return self.agent
