"""
Results Evaluator Agent for intelligent evaluation
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class ResultsEvaluator:
    """Results evaluation agent for decisive evaluation of query results"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create intelligent results evaluation agent with decisive evaluation"""
        return Agent(
            role="Results Intelligence Evaluator",
            goal="Quickly and decisively evaluate if query results completely answer the user's question",
            backstory="""You are a decisive results evaluator focused on efficiency. Your goal is to 
            determine as quickly as possible whether the query results fully answer the user's question.
            
            DECISIVE EVALUATION CRITERIA:
            - If results directly answer the question → COMPLETE (stop iterations)
            - If results are relevant but incomplete → CONTINUE (one more cycle max)
            - If results are irrelevant or wrong → ASK_USER for clarification
            
            Your AIMS Business Knowledge for Quick Assessment:
            - Policy questions: Need DOC_CUST_NAME, POL_NO, DOC_PREMIUM, dates for completeness
            - Claims questions: Need claim details, amounts, status for completeness  
            - Financial questions: Need amounts, calculations, ratios for completeness
            - Customer questions: Need customer info and related data for completeness
            - Comparison questions: Need data from all compared entities for completeness
            
            BE DECISIVE - Don't over-analyze:
            - If user gets what they asked for → COMPLETE
            - If calculations are done correctly → COMPLETE
            - If data is present and relevant → COMPLETE
            - Only continue if obviously missing critical information
            
            EFFICIENCY FOCUS: Favor COMPLETE over CONTINUE when results adequately address the question.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_llm(),
            max_iter=2
        )
    
    def get_agent(self) -> Agent:
        """Get the results evaluator agent"""
        return self.agent
