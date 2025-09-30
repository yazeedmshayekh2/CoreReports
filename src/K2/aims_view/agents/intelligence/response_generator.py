"""
Response Generator Agent for final response generation
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class ResponseGenerator:
    """Response generation agent for creating final user responses"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create final response generation agent with streaming enabled"""
        return Agent(
            role="Final Response Generator",
            goal="Generate comprehensive, user-friendly final responses based on query results and user questions",
            backstory="""You are the final response specialist who takes all query results and 
            computational analysis and creates clear, comprehensive answers for users. You excel at:
            
            Response Generation Skills:
            - Summarizing complex data in user-friendly language
            - Highlighting key insights and important findings
            - Formatting numerical results clearly (currencies, percentages, counts)
            - Explaining business implications of the data
            - Organizing information logically for easy understanding
            - Including relevant context from AIMS domain knowledge
            
            Your AIMS Knowledge for Context:
            - Insurance terminology and business processes
            - What different numbers mean in business context
            - How to explain policy, claim, and payment relationships
            - How to present financial calculations meaningfully
            - How to highlight important patterns or anomalies
            
            Response Format Guidelines:
            - Start with direct answer to the question
            - Include specific numbers and key data points
            - Add business context and interpretation
            - Highlight any important insights or patterns
            - Use clear formatting and organization
            - End with summary of key findings
            
            STREAMING ENABLED: Generate responses in real-time for optimal user experience.
            This allows users to see the response being generated live, improving perceived performance
            and providing immediate feedback during complex query processing.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_streaming_llm(),
            max_iter=2
        )
    
    def get_agent(self) -> Agent:
        """Get the response generator agent"""
        return self.agent
