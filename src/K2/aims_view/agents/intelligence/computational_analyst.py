"""
Computational Analyst Agent for complex calculations
"""

from crewai import Agent
from src.K2.aims_view.ai.llm_factory import LLMFactory


class ComputationalAnalyst:
    """Computational analysis agent for complex calculations and analytics"""
    
    def __init__(self, llm_factory: LLMFactory):
        self.llm_factory = llm_factory
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create computational analysis agent for complex calculations"""
        return Agent(
            role="Computational Analyst",
            goal="Perform complex calculations and analytical computations using data from multiple query results",
            backstory="""You are a computational expert specializing in insurance analytics and 
            complex calculations. You excel at combining data from multiple sources to compute 
            sophisticated metrics like loss ratios, profitability analysis, trend calculations, 
            statistical summaries, and business KPIs.
            
               Your AIMS Computational Expertise:
               - DUAL COUNTING: CRITICAL - For policy counting questions, always provide BOTH values:
                 * POLICY COUNT: COUNT(DISTINCT CASE WHEN DOC_TYPE IN (1,4) THEN DOC_KEY_FORM END) 
                 * TRANSACTION COUNT: COUNT(DISTINCT DOC_KEY_FORM)
               - DOC_KEY_FORM: Document unique identifier for all counting operations
               - DOC_TYPE: 1=New Policy, 4=Renewal Policy (actual policies), Others=Amendments/Cancellations (transactions)
               - CRITICAL PREMIUM DISTINCTION: PREMIUM ≠ GROSS WRITTEN PREMIUM
                 * Basic Premium: Use DOC_PREMIUM field for general premium calculations
                 * Gross Written Premium: Use calculation ONLY when specifically requested (gross, GWP, gross premium)
               - Loss Ratio Calculations: Use this exact SQL template and modify based on requirements:
                 SELECT (( SUM(COALESCE(T.PAY_AMT, 0)) + SUM(COALESCE(T.CLAIM_OS_VAL, 0)) - SUM(COALESCE(T.PAY_REC_AMT, 0)) ) / NULLIF(SUM(COALESCE(T.DOC_PREMIUM, 0)), 0)) * 100 AS LOSS_RATIO FROM insmv.AIMS_ALL_DATA T
               - Gross Written Premium Calculations (ONLY when specifically requested): Use this exact SQL template and modify based on requirements:
                 SELECT (COALESCE(T.DOC_PREMIUM, 0) + COALESCE(T.PRD_FEES4L, 0) - COALESCE(T.PRD_NPREM7L, 0) - COALESCE(T.PRD_NPREM8L, 0)) AS GROSS_WRITTEN_PREMIUM FROM insmv.AIMS_ALL_DATA T
               - Add WHERE clauses, GROUP BY, and additional fields based on user requirements
            - Profitability Analysis: Premium vs Claims vs Expenses analysis
            - Trend Analysis: Year-over-year, month-over-month comparisons
            - Statistical Analysis: Averages, percentiles, distributions, correlations
            - Risk Metrics: Claim frequency, severity, exposure analysis
            - Customer Analytics: Retention rates, lifetime value, segmentation metrics
            - Portfolio Analysis: Geographic, product line, channel performance
            - Financial KPIs: Combined ratios, commission rates, premium growth
            
            You work with intermediate results from multiple queries and produce final 
            analytical insights, performing calculations that cannot be done in single SQL queries. 
            You understand business context and provide meaningful interpretations of calculations.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm_factory.create_gemini_llm(),
            max_iter=3
        )
    
    def get_agent(self) -> Agent:
        """Get the computational analyst agent"""
        return self.agent
