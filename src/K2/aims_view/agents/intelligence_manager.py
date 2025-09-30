"""
Main Intelligence Manager - Orchestrates all AI agents for intelligent problem solving
"""

from crewai import Task, Crew, Process
from src.K2.aims_view.ai.llm_factory import LLMFactory
from src.K2.aims_view.agents.intelligence.strategic_planner import StrategicPlanner
from src.K2.aims_view.agents.intelligence.query_architect import QueryArchitect
from src.K2.aims_view.agents.intelligence.execution_specialist import ExecutionSpecialist
from src.K2.aims_view.agents.intelligence.computational_analyst import ComputationalAnalyst
from src.K2.aims_view.agents.intelligence.results_evaluator import ResultsEvaluator
from src.K2.aims_view.agents.intelligence.response_generator import ResponseGenerator
from src.K2.aims_view.agents.intelligence.schema_analyst import SchemaAnalyst
from src.K2.aims_view.agents.specialized.name_detector import NameDetector
from src.K2.aims_view.agents.specialized.customer_validator import CustomerValidator
from src.K2.aims_view.agents.specialized.name_matcher import NameMatcher
from src.K2.aims_view.core.domain_knowledge import load_aims_domain_knowledge, format_domain_knowledge_for_planning
from src.K2.aims_view.utils.context_builder import get_comprehensive_aims_knowledge_summary, build_previous_results_context
from src.K2.aims_view.utils.query_utils import clean_query, build_execution_context, format_results_summary, format_data_sources_summary
from src.K2.aims_view.database.database import SecureOracleDBUtils
import json
from datetime import datetime
import os


class IntelligentSQLManager:
    """Master Intelligence Manager for Autonomous SQL Query Generation and Problem Solving"""
    
    def __init__(self, config: dict = None):
        # Initialize database connection
        self.db_utils = SecureOracleDBUtils()
        
        # Load configuration if not provided
        if config is None:
            import json
            from pathlib import Path
            config_path = Path(__file__).parent.parent / "config.json"
            with open(config_path, "r") as f:
                config = json.load(f)
        
        # Initialize LLM factory
        self.llm_factory = LLMFactory(config)
        
        # Load AIMS database domain knowledge
        self.domain_knowledge = load_aims_domain_knowledge()
        
        # Create specialized agent instances
        self.strategy_planner = StrategicPlanner(self.llm_factory)
        self.schema_analyst = SchemaAnalyst(self.llm_factory)
        self.query_architect = QueryArchitect(self.llm_factory)
        self.execution_specialist = ExecutionSpecialist(self.llm_factory)
        self.computational_analyst = ComputationalAnalyst(self.llm_factory)
        self.results_evaluator = ResultsEvaluator(self.llm_factory)
        self.response_generator = ResponseGenerator(self.llm_factory)
        
        # Name detection and customer handling agents
        self.name_detector = NameDetector(self.llm_factory)
        self.customer_validator = CustomerValidator(self.llm_factory)
        self.name_matcher = NameMatcher(self.llm_factory)
        
        # System state and memory
        self.schema_data = {"columns": []}  # Initialize with empty schema
        self.execution_history = []
        self.accumulated_results = {}
        self.current_strategy = None
        self.confidence_threshold = 0.85
        
        from pathlib import Path
        # Memory system for conversation context
        self.memory_file = Path(__file__).parent.parent / "memory" / "conversation_memory.json"
        self.memory_size = 5
        self.memory = self._load_memory()
    
    def solve_intelligently(self, user_question: str, max_cycles: int = 5) -> dict:
        """Master Intelligence Method - Orchestrates complete problem solving with smart retry logic"""
        
        print(f"🚀 MASTER INTELLIGENCE MANAGER ACTIVATED")
        print(f"🎯 Question: {user_question}")
        print("="*80)
        
        self.execution_history = []
        self.accumulated_results = {}
        
        try:
            # Initialize enhanced_question with original question
            enhanced_question = user_question
            customer_context = ""
            
            # Check memory for relevant context
            memory_context = self._get_memory_context(user_question)
            if memory_context:
                print("💭 MEMORY: Found relevant context from previous conversations")
                enhanced_question = memory_context + enhanced_question
            
            # PHASE 0: Name Detection and Customer Identification
            name_handling_result = self.detect_and_handle_names(user_question)
            
            if not name_handling_result.get('proceed', True):
                # Name detection found issues that prevent proceeding
                if name_handling_result.get('status') == 'cancelled':
                    return {
                        'status': 'cancelled',
                        'message': 'User cancelled the customer identification process',
                        'cycles_used': 0
                    }
                elif name_handling_result.get('status') == 'not_implemented':
                    return {
                        'status': 'not_implemented',
                        'message': f"{name_handling_result.get('classification')} name handling not yet implemented",
                        'cycles_used': 0
                    }
                else:
                    return {
                        'status': 'error',
                        'message': f"Name handling failed: {name_handling_result.get('status')}",
                        'cycles_used': 0
                    }
            
            # If we have customer/company data, add it to the question context
            if name_handling_result.get('status') == 'valid':
                if 'customer_data' in name_handling_result:
                    customer_data = name_handling_result['customer_data'][0]  # First customer
                    customer_name = customer_data.get('DOC_CUST_NAME', '')
                    customer_id = customer_data.get('CUST_ID_NO', '')
                    company_id = customer_data.get('COMP_EID_NO', '')
                    
                    if customer_id:
                        customer_context = f"\nCUSTOMER CONTEXT: Individual customer '{customer_name}' with ID: {customer_id}"
                        enhanced_question = f"{user_question} (Focus on customer with CUST_ID_NO = '{customer_id}')"
                    elif company_id:
                        customer_context = f"\nCUSTOMER CONTEXT: Company customer '{customer_name}' with ID: {company_id}"
                        enhanced_question = f"{user_question} (Focus on company customer with COMP_EID_NO = '{company_id}')"
                    
                    print(f"✅ Customer identified: {customer_name}")
                    print(f"🎯 Enhanced question: {enhanced_question}")
                
                elif 'customer_name' in name_handling_result:
                    # Handle simple customer name context
                    customer_name = name_handling_result['customer_name']
                    customer_context = f"\nCUSTOMER CONTEXT: Customer '{customer_name}'"
                    enhanced_question = f"{user_question} (Focus on customer named '{customer_name}' - search by DOC_CUST_NAME)"
                    
                    print(f"✅ Customer name identified: {customer_name}")
                    print(f"🎯 Enhanced question: {enhanced_question}")
                
                elif 'broker_name' in name_handling_result:
                    broker_name = name_handling_result['broker_name']
                    customer_context = f"\nBROKER CONTEXT: Agent/Broker '{broker_name}'"
                    enhanced_question = f"{user_question} (Focus on policies/transactions involving agent DOC_AGENT_NAME = '{broker_name}')"
                    
                    print(f"✅ Broker identified: {broker_name}")
                    print(f"🎯 Enhanced question: {enhanced_question}")
                
                elif 'user_name' in name_handling_result:
                    user_name = name_handling_result['user_name']
                    customer_context = f"\nUSER CONTEXT: System User '{user_name}'"
                    enhanced_question = f"{user_question} (Focus on policies/transactions involving system user DOC_USER_NAME = '{user_name}')"
                    
                    print(f"✅ System User identified: {user_name}")
                    print(f"🎯 Enhanced question: {enhanced_question}")
            
            # PHASE 1: Strategic Planning (happens once at the beginning)
            print(f"\n🧠 STRATEGIC PLANNING PHASE")
            print("-" * 60)
            
            strategy_result = self._execute_strategic_planning(enhanced_question, 1)
            
            if strategy_result.get('action') == 'ASK_USER':
                # User clarification needed
                return self._handle_user_clarification(strategy_result, user_question)
            
            if strategy_result.get('action') not in ['QUERY_DIRECT', 'QUERY_SEQUENCE', 'QUERY_COMPUTE']:
                print(f"⚠️  Unknown strategy action: {strategy_result.get('action')}, defaulting to QUERY_DIRECT")
                strategy_result['action'] = 'QUERY_DIRECT'
            
            # PHASE 2: Query Execution with Smart Retry (built-in retry logic)
            print(f"\n🔧 QUERY EXECUTION PHASE")
            print("-" * 60)
            
            execution_result = self._execute_query_phase(strategy_result, enhanced_question)
            
            # Check if execution was successful (has results without errors)
            has_successful_results = False
            has_errors = False
            
            for key, result in execution_result.get('results', {}).items():
                if 'error' in result:
                    has_errors = True
                elif 'results' in result and result.get('row_count', 0) >= 0:
                    has_successful_results = True
            
            # If we have successful results, immediately generate final response
            if has_successful_results:
                print(f"✅ Queries executed successfully - Generating final response immediately...")
                
                # Create a successful evaluation result
                mock_evaluation = {
                    'status': 'COMPLETE',
                    'confidence': 0.9,
                    'summary': 'Queries executed successfully with data retrieved'
                }
                
                final_response = self._generate_final_response(
                    mock_evaluation, execution_result, enhanced_question, 1
                )
                return final_response
            
            # If we have errors but no successful results, try strategic re-planning (fallback cycles)
            if has_errors and not has_successful_results:
                print(f"⚠️  All queries failed, attempting strategic re-planning...")
                
                cycle = 1
                while cycle < max_cycles:
                    cycle += 1
                    print(f"\n🔄 FALLBACK CYCLE {cycle}/{max_cycles}")
                    print("-" * 60)
                    
                    try:
                        # Re-plan strategy with error context
                        strategy_result = self._execute_strategic_planning(
                            f"{enhanced_question} (Previous queries failed, need alternative approach)", cycle
                        )
                        
                        if strategy_result.get('action') == 'ASK_USER':
                            return self._handle_user_clarification(strategy_result, enhanced_question)
                        
                        # Execute with new strategy
                        execution_result = self._execute_query_phase(strategy_result, enhanced_question)
                        
                        # Check results again
                        has_successful_results = False
                        for key, result in execution_result.get('results', {}).items():
                            if 'results' in result and result.get('row_count', 0) >= 0 and 'error' not in result:
                                has_successful_results = True
                                break
                        
                        if has_successful_results:
                            print(f"✅ Fallback strategy successful - Generating final response...")
                            mock_evaluation = {
                                'status': 'COMPLETE',
                                'confidence': 0.85,
                                'summary': f'Problem solved using fallback strategy in cycle {cycle}'
                            }
                            final_response = self._generate_final_response(
                                mock_evaluation, execution_result, enhanced_question, cycle
                            )
                            return final_response
                        
                    except Exception as e:
                        print(f"❌ Error in fallback cycle {cycle}: {str(e)}")
                        if cycle == max_cycles:
                            # Generate error response
                            mock_execution = {'results': {}, 'executed_queries': [], 'action': 'ERROR'}
                            mock_evaluation = {
                                'status': 'ERROR', 
                                'confidence': 0.3, 
                                'summary': f'System encountered persistent errors: {str(e)}'
                            }
                            return self._generate_final_response(mock_evaluation, mock_execution, enhanced_question, cycle)
                        continue
                
                # If we exhaust all cycles, generate response with partial results
                return self._format_partial_response(enhanced_question, max_cycles)
            
            # If we have no results at all, generate error response
            mock_execution = {'results': {}, 'executed_queries': [], 'action': 'NO_RESULTS'}
            mock_evaluation = {
                'status': 'ERROR',
                'confidence': 0.3,
                'summary': 'No results could be retrieved from the database'
            }
            return self._generate_final_response(mock_evaluation, mock_execution, enhanced_question, 1)
            
        except Exception as e:
            print(f"❌ Critical error in solve_intelligently: {str(e)}")
            # Generate final error response
            mock_execution = {'results': {}, 'executed_queries': [], 'action': 'CRITICAL_ERROR'}
            mock_evaluation = {
                'status': 'ERROR', 
                'confidence': 0.2, 
                'summary': f'Critical system error: {str(e)}'
            }
            # Use enhanced_question if available, otherwise fall back to original
            question_to_use = enhanced_question if 'enhanced_question' in locals() else user_question
            return self._generate_final_response(mock_evaluation, mock_execution, question_to_use, 1)
    
    # ======= MEMORY SYSTEM METHODS =======
    
    def _load_memory(self) -> dict:
        """Load conversation memory from JSON file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    memory = json.load(f)
                    return memory
            else:
                # Create initial memory structure
                return {
                    "memory_size": self.memory_size,
                    "current_session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "conversations": [],
                    "last_updated": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"⚠️ Error loading memory: {str(e)}")
            return {
                "memory_size": self.memory_size,
                "current_session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "conversations": [],
                "last_updated": datetime.now().isoformat()
            }
    
    def _save_memory(self, question: str, answer: str, metadata: dict = None):
        """Save Q&A pair to memory"""
        try:
            # Create memory directory if it doesn't exist
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            conversation_entry = {
                "timestamp": datetime.now().isoformat(),
                "session_id": self.memory.get("current_session_id", f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                "question": question,
                "answer": answer,
                "metadata": metadata or {}
            }
            
            # Add to conversations list
            self.memory["conversations"].append(conversation_entry)
            
            # Keep only last N conversations
            if len(self.memory["conversations"]) > self.memory_size:
                self.memory["conversations"] = self.memory["conversations"][-self.memory_size:]
            
            self.memory["last_updated"] = datetime.now().isoformat()
            
            # Save to file
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Error saving memory: {str(e)}")
    
    def _get_memory_context(self, current_question: str) -> str:
        """Extract relevant context from memory for current question"""
        if not self.memory.get("conversations"):
            return ""
        
        context_parts = []
        
        # Check if current question relates to previous conversations
        for conv in reversed(self.memory["conversations"][-3:]):  # Check last 3 conversations
            prev_question = conv.get("question", "")
            prev_answer = conv.get("answer", "")
            
            # Simple context detection - check for common elements
            if self._is_related_question(current_question, prev_question):
                # Extract key information from previous conversation
                extracted_info = self._extract_key_info(prev_question, prev_answer)
                if extracted_info:
                    context_parts.append(f"Previous context: {extracted_info}")
        
        if context_parts:
            return "MEMORY CONTEXT FROM RECENT CONVERSATIONS:\n" + "\n".join(context_parts) + "\n\n"
        
        return ""
    
    def _is_related_question(self, current: str, previous: str) -> bool:
        """Check if current question relates to previous one"""
        # Simple keyword-based matching for customer IDs, names, etc.
        import re
        
        # Extract potential customer IDs (11 digit numbers)
        current_ids = re.findall(r'\b\d{11}\b', current)
        previous_ids = re.findall(r'\b\d{11}\b', previous)
        
        # Check for common customer IDs
        if current_ids and previous_ids and any(id in previous_ids for id in current_ids):
            return True
        
        # Extract potential customer names (words starting with capital letters)
        current_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', current)
        previous_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', previous)
        
        # Check for common names
        if current_names and previous_names and any(name in previous_names for name in current_names):
            return True
        
        # Check for common keywords indicating continuation
        continuation_keywords = ['same', 'this', 'that', 'also', 'additionally', 'more', 'further']
        if any(keyword in current.lower() for keyword in continuation_keywords):
            return True
        
        return False
    
    def _extract_key_info(self, question: str, answer: str) -> str:
        """Extract key information from previous Q&A"""
        import re
        
        key_info = []
        
        # Extract customer IDs
        customer_ids = re.findall(r'\b\d{11}\b', question + " " + answer)
        if customer_ids:
            key_info.append(f"Customer ID(s): {', '.join(set(customer_ids))}")
        
        # Extract customer names from context
        names = re.findall(r'customer[^,\.]*?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', question + " " + answer, re.IGNORECASE)
        if names:
            key_info.append(f"Customer name(s): {', '.join(set(names))}")
        
        # Extract key numbers/counts from answer
        numbers = re.findall(r'(\d+)\s+(?:policies|claims|transactions|customers)', answer, re.IGNORECASE)
        if numbers:
            key_info.append(f"Previous results: {', '.join(numbers)} items found")
        
        return " | ".join(key_info) if key_info else ""
    
    def detect_and_handle_names(self, user_question: str) -> dict:
        """Detect names in user questions and handle customer/company identification"""
        print("🔍 PHASE 0: Name Detection and Customer Identification")
        print("-" * 60)
        
        # Step 1: Detect if the question contains names and classify them
        name_detection_result = self._detect_names_in_question(user_question)
        
        if name_detection_result['classification'] == 'NONE':
            print("✅ No names detected - proceeding with normal query processing")
            return {'status': 'no_names', 'proceed': True}
        
        print(f"🎯 Name detected: '{name_detection_result['name']}' - Type: {name_detection_result['classification']}")
        
        # Step 2: Handle based on classification
        if name_detection_result['classification'] == 'CUSTOMER':
            print(f"👤 Customer name handling is implemented")
            return self._handle_customer_identification(name_detection_result, user_question)
        elif name_detection_result['classification'] == 'AGENT':
            print(f"🏢 Processing agent/broker name handling")
            return self._handle_agent_identification(name_detection_result, user_question)
        elif name_detection_result['classification'] == 'USER':
            print(f"👨‍💼 Processing system user name handling")
            return self._handle_user_identification(name_detection_result, user_question)
        else:
            print(f"⚠️  {name_detection_result['classification']} name handling not recognized")
            return {
                'status': 'unknown_classification',
                'classification': name_detection_result['classification'],
                'proceed': False
            }
    
    def _detect_names_in_question(self, user_question: str) -> dict:
        """Use AI agent to detect and classify names in the question"""
        
        detection_task = Task(
            description=f"""Analyze this user question to detect and classify any names mentioned:

USER QUESTION: "{user_question}"

Your task is to:
1. Identify if there are any personal names or user references
2. Extract the specific name(s) mentioned
3. Classify each name based on context

CLASSIFICATION RULES:
- CUSTOMER: Names in context like "find customer John", "policies for Sarah", "John Smith's insurance"
- AGENT: Names in context like "agent Mohammed", "broker Ali", "sold by Ahmad", "written by Hassan"
         IMPORTANT: AGENT and BROKER are IDENTICAL - both refer to insurance agents/brokers
- USER: Names referring to system users like "user Ahmed", "processed by user Sarah", "created by user Ali"
        NOTE: These are database users stored in DOC_USER_NO, DOC_USER_NAME columns
- NONE: No names detected

Return your analysis in JSON format:
{{"classification": "CUSTOMER/AGENT/USER/NONE", "name": "extracted_name_or_null", "confidence": 0.95, "context": "explanation_of_why_this_classification"}}""",
            expected_output="Name detection results in JSON format",
            agent=self.name_detector.get_agent()
        )
        
        crew = Crew(agents=[self.name_detector.get_agent()], tasks=[detection_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            import re
            
            # Extract JSON from markdown code blocks if present
            result_clean = result.strip()
            
            # Look for JSON wrapped in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', result_clean, re.DOTALL | re.IGNORECASE)
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # Look for JSON wrapped in plain code blocks
                code_match = re.search(r'```\s*(.*?)\s*```', result_clean, re.DOTALL)
                if code_match:
                    json_content = code_match.group(1).strip()
                else:
                    # No code blocks, use raw result
                    json_content = result_clean
            
            # Try to find JSON-like structure if above methods fail
            if not json_content.strip().startswith('{'):
                # Look for JSON object pattern anywhere in the text
                json_pattern = re.search(r'\{.*\}', result_clean, re.DOTALL)
                if json_pattern:
                    json_content = json_pattern.group(0)
                else:
                    json_content = result_clean
            
            parsed_result = js.loads(json_content)
            return parsed_result
        except Exception as e:
            # Fallback parsing
            print(f"⚠️ JSON parsing failed for name detection: {str(e)}")
            return {"classification": "NONE", "name": None, "confidence": 0.5, "context": "Parsing failed"}
    
    def _handle_customer_identification(self, name_result: dict, user_question: str) -> dict:
        """Handle customer identification process"""
        customer_name = name_result['name']
        print(f"👤 Processing customer: {customer_name}")
        
        # Ask user for customer ID or phone number
        print(f"\n💡 To find customer '{customer_name}', I need additional information:")
        print("1️⃣  Customer ID (11 digits - numbers or characters)")
        print("2️⃣  Phone number (8-11 digits)")
        print("3️⃣  Company ID (if this is a company customer)")
        
        while True:
            user_input = input("🔍 Please provide Customer ID, Phone number, or Company ID: ").strip()
            
            if not user_input:
                print("❌ Please provide valid identification")
                continue
            
            # Validate and process the input
            validation_result = self._validate_customer_input(user_input, customer_name)
            
            if validation_result['status'] == 'valid':
                return validation_result
            elif validation_result['status'] == 'multiple_matches':
                # Handle multiple customers with same phone
                return self._handle_multiple_customer_matches(validation_result, customer_name, user_question)
            else:
                print(f"❌ {validation_result['message']}")
                continue
    
    def _handle_agent_identification(self, name_result: dict, user_question: str) -> dict:
        """Handle agent/broker identification process"""
        agent_name = name_result['name']
        print(f"🏢 Processing agent/broker: {agent_name}")
        
        print(f"\n💡 Searching for agent/broker '{agent_name}' in database...")
        
        # Extract branch context from user question for intelligent filtering
        branch_context = self._extract_branch_context(user_question)
        if branch_context:
            print(f"🏢 Branch context detected: {branch_context}")
        
        # Get available broker names from database (filtered by branch if specified)
        available_brokers = self._get_all_broker_names(branch_filter=branch_context)
        
        if not available_brokers:
            return {
                'status': 'invalid',
                'message': 'No broker names found in database',
                'proceed': False
            }
        
        print(f"📊 Found {len(available_brokers)} brokers in database")
        
        # Use intelligent matching to find possible broker matches
        match_result = self._intelligent_broker_matching(agent_name, available_brokers)
        
        if match_result['status'] == 'exact_match':
            # Single exact match found
            selected_broker = match_result['broker']
            print(f"✅ Exact match found: {selected_broker}")
            return {
                'status': 'valid',
                'broker_name': selected_broker,
                'search_type': 'AGENT_NAME',
                'proceed': True
            }
        elif match_result['status'] == 'multiple_matches':
            # Multiple matches found, let user select
            return self._handle_multiple_broker_matches(match_result, agent_name, user_question)
        elif match_result['status'] == 'no_match':
            print(f"❌ No broker matches found for '{agent_name}'")
            print("🔍 Here are some available broker names for reference:")
            
            # Show first 10 broker names as examples
            for i, broker in enumerate(available_brokers[:10], 1):
                print(f"   {i}. {broker}")
            
            if len(available_brokers) > 10:
                print(f"   ... and {len(available_brokers) - 10} more")
            
            return {
                'status': 'invalid',
                'message': f"No broker found matching '{agent_name}'. Please check the name and try again.",
                'proceed': False
            }
        else:
            return {
                'status': 'invalid',
                'message': f"Broker matching failed: {match_result.get('message', 'Unknown error')}",
                'proceed': False
            }
    
    def _handle_user_identification(self, name_result: dict, user_question: str) -> dict:
        """Handle system user identification process"""
        user_name = name_result['name']
        print(f"👨‍💼 Processing system user: {user_name}")
        
        print(f"\n💡 Searching for system user '{user_name}' in database...")
        
        # Extract branch context from user question for intelligent filtering
        branch_context = self._extract_branch_context(user_question)
        if branch_context:
            print(f"🏢 Branch context detected: {branch_context}")
        
        # Get available user names from database (filtered by branch if specified)
        available_users = self._get_all_user_names(branch_filter=branch_context)
        
        if not available_users:
            return {
                'status': 'invalid',
                'message': 'No system users found in database',
                'proceed': False
            }
        
        print(f"📊 Found {len(available_users)} system users in database")
        
        # Use intelligent matching to find possible user matches
        match_result = self._intelligent_user_matching(user_name, available_users)
        
        if match_result['status'] == 'exact_match':
            # Single exact match found
            selected_user = match_result['user']
            print(f"✅ Exact match found: {selected_user}")
            return {
                'status': 'valid',
                'user_name': selected_user,
                'search_type': 'USER_NAME',
                'proceed': True
            }
        elif match_result['status'] == 'multiple_matches':
            # Multiple matches found, let user select
            return self._handle_multiple_user_matches(match_result, user_name, user_question)
        elif match_result['status'] == 'no_match':
            print(f"❌ No user matches found for '{user_name}'")
            print("🔍 Here are some available system users for reference:")
            
            # Show first 10 user names as examples
            for i, user in enumerate(available_users[:10], 1):
                print(f"   {i}. {user}")
            
            if len(available_users) > 10:
                print(f"   ... and {len(available_users) - 10} more")
            
            return {
                'status': 'invalid',
                'message': f"No system user found matching '{user_name}'. Please check the name and try again.",
                'proceed': False
            }
        else:
            return {
                'status': 'invalid',
                'message': f"User matching failed: {match_result.get('message', 'Unknown error')}",
                'proceed': False
            }
    
    def _execute_strategic_planning(self, user_question: str, cycle: int) -> dict:
        """PHASE 1: Strategic Planning and Decision Making"""
        print("📋 PHASE 1: Strategic Planning")
        
        # Build context from previous cycles
        context = build_execution_context(self.execution_history, self.accumulated_results, cycle)
        
        # Incorporate domain knowledge
        domain_context = format_domain_knowledge_for_planning(self.domain_knowledge, user_question)
        
        # Check for memory context
        memory_context = self._get_memory_context(user_question)
        
        planning_task = Task(
            description=f"""As the Strategic Query Planner, analyze this question using comprehensive AIMS database knowledge:

QUESTION: {user_question}
CYCLE: {cycle}
PREVIOUS CONTEXT: {context}
{memory_context}
{get_comprehensive_aims_knowledge_summary()}

QUESTION-SPECIFIC CONTEXT:
{domain_context}

Create a strategic plan that includes:
1. IMMEDIATE ACTION: What should be done right now?
   - QUERY_DIRECT: Can answer directly with one optimal query
   - QUERY_SEQUENCE: Needs multiple queries in sequence (specify order and data flow)
   - QUERY_COMPUTE: Needs queries plus computational analysis (specify calculation steps)
   - ASK_USER: Need user clarification first (specify what to ask)

2. EXECUTION STEPS: If querying, break into logical steps with data flow:
   - Step 1: [Query purpose, target data, expected output]
   - Step 2: [How it uses Step 1 results, additional data needed]
   - Step 3: [Computation/Analysis using previous results]
   - etc.

3. COMPUTATIONAL REQUIREMENTS: If complex calculations needed:
   - Data sources required from each query
   - Calculation formulas and business logic
   - Expected final output format

4. SUCCESS CRITERIA: How to know when complete

5. RISK ASSESSMENT: What could go wrong?

Respond with JSON format:
{{"action": "QUERY_DIRECT/QUERY_SEQUENCE/QUERY_COMPUTE/ASK_USER", "steps": [...], "computational_requirements": {{"formulas": "...", "data_sources": "..."}}, "rationale": "...", "success_criteria": "..."}}""",
            expected_output="Strategic execution plan in JSON format",
            agent=self.strategy_planner.get_agent()
        )
        
        crew = Crew(agents=[self.strategy_planner.get_agent()], tasks=[planning_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            parsed_result = js.loads(result.strip())
            
            # Ensure steps is always a list of strings
            if 'steps' in parsed_result:
                if not isinstance(parsed_result['steps'], list):
                    parsed_result['steps'] = [str(parsed_result['steps'])]
                else:
                    parsed_result['steps'] = [str(step) if not isinstance(step, str) else step for step in parsed_result['steps']]
            
            return parsed_result
        except:
            # Fallback parsing
            return {"action": "QUERY_DIRECT", "steps": [str(result)], "rationale": str(result), "computational_requirements": None}
    
    def _execute_query_phase(self, strategy_result: dict, user_question: str) -> dict:
        """PHASE 2: Query Architecture & Execution with Multi-step Processing and Smart Retry Logic"""
        print("🔧 PHASE 2: Query Architecture & Execution")
        
        executed_queries = []
        results = {}
        intermediate_data = {}
        action = strategy_result.get('action', 'QUERY_DIRECT')
        
        steps = strategy_result.get('steps', [])
        
        # Execute SQL queries first with retry logic
        query_steps = []
        for step in steps:
            step_str = str(step) if not isinstance(step, str) else step
            if not step_str.lower().startswith('compute') and not step_str.lower().startswith('calculate'):
                query_steps.append(step_str)
        
        for i, step in enumerate(query_steps):
            print(f"   Step {i+1}: {step}")
            
            # Build context from previous results for data flow
            previous_results_context = build_previous_results_context(intermediate_data)
            
            # Retry logic for each query step (up to 3 attempts)
            max_query_retries = 3
            step_successful = False
            last_error = None
            
            for retry_attempt in range(max_query_retries):
                if retry_attempt > 0:
                    print(f"   🔄 Retry attempt {retry_attempt + 1}/{max_query_retries} for Step {i+1}")
                
                # Design the query with domain knowledge and previous results
                domain_context = format_domain_knowledge_for_planning(self.domain_knowledge, user_question)
                
                # Add retry context if this is a retry
                retry_context = ""
                if retry_attempt > 0 and last_error:
                    retry_context = f"\nPREVIOUS ATTEMPT FAILED: {last_error}\nPlease generate an alternative query to avoid this error.\n"
                
                query_task = Task(
                    description=f"""As the SQL Query Architect, design an optimal query using comprehensive AIMS database knowledge:

USER QUESTION: {user_question}
CURRENT STEP: {step}
STRATEGY ACTION: {action}
AVAILABLE COLUMNS: [DOC_SERIAL, DOC_CUST_NAME, CUST_ID_NO, DOC_PREMIUM, DOC_MAJ_NAME, etc.]
{previous_results_context}
{retry_context}

{get_comprehensive_aims_knowledge_summary()}

STEP-SPECIFIC CONTEXT:
{domain_context}

Design a precise Oracle SQL query that:
1. Targets table: insmv.AIMS_ALL_DATA  
2. Uses appropriate columns based on AIMS domain knowledge
3. Applies correct business rules and relationships
4. Includes proper WHERE clauses with domain-aware filters
5. Optimizes for performance and accuracy
6. Returns meaningful results for the user's question
7. Considers data from previous steps for multi-step analysis

Generate ONLY the SQL query without trailing semicolon, no explanations.""",
                    expected_output="Complete Oracle SQL query",
                    agent=self.query_architect.get_agent()
                )
                
                crew = Crew(agents=[self.query_architect.get_agent()], tasks=[query_task], process=Process.sequential, memory=False)
                sql_query = str(crew.kickoff()).strip()
                
                # Clean and execute the query
                sql_query = clean_query(sql_query)
                
                try:
                    print(f"   🎯 Executing: {sql_query[:100]}...")
                    query_results = self.db_utils._safe_execute_query(sql_query)
                    executed_queries.append(sql_query)
                    
                    # Store results for next steps to use
                    step_key = f"step_{i+1}"
                    step_result = {
                        'query': sql_query,
                        'results': query_results.to_dict('records') if hasattr(query_results, 'to_dict') else query_results,
                        'row_count': len(query_results),
                        'step_description': step,
                        'retry_attempts': retry_attempt + 1
                    }
                    results[step_key] = step_result
                    intermediate_data[step_key] = step_result
                    
                    print(f"   ✅ Step {i+1} completed: {len(query_results)} rows (attempt {retry_attempt + 1})")
                    step_successful = True
                    break  # Success - exit retry loop
                    
                except Exception as e:
                    last_error = str(e)
                    print(f"   ❌ Step {i+1} attempt {retry_attempt + 1} failed: {last_error}")
                    
                    if retry_attempt == max_query_retries - 1:
                        # Final attempt failed - store error result
                        step_result = {
                            'query': sql_query,
                            'error': last_error,
                            'row_count': 0,
                            'step_description': step,
                            'retry_attempts': retry_attempt + 1
                        }
                        results[f"step_{i+1}"] = step_result
                        intermediate_data[f"step_{i+1}"] = step_result
                        print(f"   ❌ Step {i+1} failed after {max_query_retries} attempts")
            
            # If any step fails completely, we might want to continue with partial results
            if not step_successful:
                print(f"   ⚠️  Step {i+1} could not be executed successfully after {max_query_retries} attempts")
        
        # Execute computational analysis if needed
        if action == 'QUERY_COMPUTE':
            computational_steps = []
            for step in steps:
                step_str = str(step) if not isinstance(step, str) else step
                if step_str.lower().startswith('compute') or step_str.lower().startswith('calculate'):
                    computational_steps.append(step_str)
            
            for i, comp_step in enumerate(computational_steps):
                print(f"   📊 Computational Step {i+1}: {comp_step}")
                
                comp_result = self._execute_computational_analysis(
                    comp_step, 
                    intermediate_data, 
                    user_question, 
                    strategy_result.get('computational_requirements', {})
                )
                
                comp_key = f"computation_{i+1}"
                results[comp_key] = comp_result
                intermediate_data[comp_key] = comp_result
                
                print(f"   ✅ Computational Step {i+1} completed")
        
        return {
            'executed_queries': executed_queries,
            'results': results,
            'strategy': strategy_result,
            'action': action,
            'intermediate_data': intermediate_data
        }
    
    def _execute_computational_analysis(self, comp_step: str, intermediate_data: dict, user_question: str, comp_requirements: dict) -> dict:
        """Execute computational analysis using intermediate query results"""
        
        # Format data sources for the computational analyst
        data_summary = format_data_sources_summary(intermediate_data)
        
        computation_task = Task(
            description=f"""As the Computational Analyst, perform complex calculations using the provided data:

USER QUESTION: {user_question}
COMPUTATIONAL STEP: {comp_step}
COMPUTATIONAL REQUIREMENTS: {comp_requirements}

{data_summary}

Your task is to:
1. Analyze the available data from previous query steps
2. Perform the required calculations based on the computational step
3. Apply appropriate business logic and formulas
4. Provide clear numerical results with business context
5. Include any relevant insights or observations

Return your analysis in JSON format with:
{{"calculation_type": "...", "formula_used": "...", "result": "...", "business_interpretation": "...", "data_points_used": "..."}}""",
            expected_output="Computational analysis results in structured format",
            agent=self.computational_analyst.get_agent()
        )
        
        crew = Crew(agents=[self.computational_analyst.get_agent()], tasks=[computation_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            comp_result = js.loads(result.strip())
        except:
            # Fallback if JSON parsing fails
            comp_result = {
                "calculation_type": comp_step,
                "result": result,
                "formula_used": "Analysis provided",
                "business_interpretation": result,
                "data_points_used": list(intermediate_data.keys())
            }
        
        return comp_result
    
    def _generate_final_response(self, evaluation_result: dict, execution_result: dict, user_question: str, cycle: int) -> dict:
        """Generate final user-friendly response using the response generator agent"""
        
        # Format execution results for response generation
        results_summary = format_results_summary(execution_result)
        
        response_task = Task(
            description=f"""As the Final Response Generator, create a comprehensive, user-friendly response:

USER QUESTION: {user_question}
EVALUATION RESULT: {evaluation_result}

{results_summary}

Your task is to generate a clear, comprehensive final response that:

1. DIRECTLY ANSWERS the user's question in the first paragraph
2. PRESENTS KEY DATA clearly with proper formatting
3. PROVIDES BUSINESS CONTEXT using AIMS domain knowledge
4. HIGHLIGHTS IMPORTANT INSIGHTS from the data
5. ORGANIZES information logically for easy reading
6. INCLUDES RELEVANT NUMBERS with appropriate units/formatting

Generate a professional, informative response that fully addresses the user's question.""",
            expected_output="Comprehensive, user-friendly final response",
            agent=self.response_generator.get_agent()
        )
        
        crew = Crew(agents=[self.response_generator.get_agent()], tasks=[response_task], process=Process.sequential, memory=False)
        
        print("\n📋 GENERATING COMPREHENSIVE RESPONSE:")
        print("="*70)
        print("🔄 Streaming response generation in progress...")
        print("📡 Real-time AI response streaming enabled...")
        print("⏳ Please wait while the response is generated live...")
        print()
        
        # Execute with streaming enabled
        result = crew.kickoff()
        final_response_text = str(result)
        
        print()
        print("="*70)
        print("✅ Response generation completed!")
        
        # Save to memory
        metadata = {
            'confidence': evaluation_result.get('confidence', 0.95),
            'cycles_used': cycle,
            'status': 'success',
            'query_type': execution_result.get('action', 'QUERY'),
            'queries_executed': len(execution_result.get('executed_queries', []))
        }
        self._save_memory(user_question, final_response_text, metadata)
        
        return {
            'status': 'success',
            'question': user_question,
            'response': final_response_text,
            'cycles_used': cycle,
            'confidence': evaluation_result.get('confidence', 0.95),
            'execution_summary': execution_result,
            'evaluation_summary': evaluation_result
        }
    
    def _handle_user_clarification(self, clarification_request: dict, user_question: str) -> dict:
        """Handle user clarification requests intelligently"""
        print(f"\n🤔 Intelligent Clarification Needed")
        print(f"Reason: {clarification_request.get('rationale', 'Additional information needed')}")
        
        # For now, return a placeholder response
        return {
            'status': 'clarification_needed',
            'message': 'User clarification would be helpful but interactive mode not implemented in modular version',
            'question': user_question
        }
    
    def _format_partial_response(self, user_question: str, max_cycles: int) -> dict:
        """Format partial response when max cycles reached"""
        print(f"\n⚠️  Reached maximum cycles ({max_cycles})")
        print(f"📋 Generating best available response...")
        
        # Create a mock execution result from accumulated results
        mock_execution = {
            'results': self.accumulated_results,
            'executed_queries': self.execution_history,
            'action': 'PARTIAL'
        }
        
        # Create a partial evaluation result
        mock_evaluation = {
            'status': 'PARTIAL',
            'confidence': 0.7,
            'summary': 'Partial solution - reached maximum cycles'
        }
        
        # Generate final response even for partial results
        result = self._generate_final_response(mock_evaluation, mock_execution, user_question, max_cycles)
        
        # Save partial result to memory
        metadata = {
            'confidence': 0.7,
            'cycles_used': max_cycles,
            'status': 'partial',
            'query_type': 'PARTIAL',
            'queries_executed': len(self.execution_history)
        }
        self._save_memory(user_question, result.get('response', 'Partial solution provided'), metadata)
        
        return result
    
    def load_schema_data(self):
        """Load and cache database schema and sample data"""
        if self.schema_data is None:
            print("🔍 Loading database schema and sample data...")
            self.schema_data = self.db_utils.get_table_schema_and_sample_data()
            print(f"✅ Loaded {self.schema_data['total_columns']} columns and {self.schema_data['sample_row_count']} sample rows")
        return self.schema_data
    
    def _extract_branch_context(self, user_question: str) -> list:
        """Extract branch names mentioned in the user question using AI"""
        try:
            branch_extraction_task = Task(
                description=f"""Extract branch names mentioned in this user question:

USER QUESTION: "{user_question}"

Your task is to identify any branch names mentioned in the question. Look for:

KNOWN BRANCH PATTERNS:
- "main branch", "head office", "headquarters" → ["main"]
- "doha branch", "doha islamic", "shamel" → ["doha", "shamel"] 
- "india branch", "ifsc" → ["india"]
- "mena life", "lebanon" → ["mena life", "lebanon"]
- "mena re", "dubai" → ["mena re", "dubai"]
- Location-based: "al rayyan", "al khor", "lulu", etc. → specific office names

SEARCH PATTERNS:
- Words: branch, office, headquarters, main, head, regional, location
- Specific branch names from AIMS system
- Geographic locations that indicate branches
- Arabic/English transliterations

IMPORTANT: Be flexible but accurate. Look for both explicit branch mentions and implied location references.

Return ONLY a JSON list of branch identifiers found:
["identifier1", "identifier2"] or []

Examples:
- "Show me agents in main branch" → ["main"]
- "Find brokers in Doha Islamic branch" → ["doha islamic", "shamel"]
- "List all agents" → []
- "Head office and India branch users" → ["main", "india"]""",
                expected_output="JSON list of branch identifiers",
                agent=self.name_detector.get_agent()  # Reuse existing agent
            )
            
            crew = Crew(agents=[self.name_detector.get_agent()], tasks=[branch_extraction_task], process=Process.sequential, memory=False)
            result = str(crew.kickoff()).strip()
            
            try:
                import json as js
                import re
                
                # Extract JSON from markdown code blocks if present
                result_clean = result.strip()
                
                # Look for JSON wrapped in markdown code blocks
                json_match = re.search(r'```json\s*(.*?)\s*```', result_clean, re.DOTALL | re.IGNORECASE)
                if json_match:
                    json_content = json_match.group(1).strip()
                else:
                    # Look for JSON wrapped in plain code blocks
                    code_match = re.search(r'```\s*(.*?)\s*```', result_clean, re.DOTALL)
                    if code_match:
                        json_content = code_match.group(1).strip()
                    else:
                        # No code blocks, use raw result
                        json_content = result_clean
                
                # Try to find JSON array pattern anywhere in the text
                if not json_content.strip().startswith('['):
                    # Look for JSON array pattern anywhere in the text
                    json_pattern = re.search(r'\[.*?\]', result_clean, re.DOTALL)
                    if json_pattern:
                        json_content = json_pattern.group(0)
                    else:
                        # If no JSON array found, return empty list
                        return []
                
                branches = js.loads(json_content)
                
                # Clean and validate branch names
                if isinstance(branches, list):
                    cleaned_branches = []
                    for branch in branches:
                        if isinstance(branch, str) and branch.strip():
                            cleaned_branches.append(branch.strip().lower())
                    return cleaned_branches
                else:
                    return []
                    
            except Exception as parse_error:
                print(f"⚠️ Branch extraction parsing failed: {str(parse_error)}")
                return []
                
        except Exception as e:
            print(f"⚠️ Branch context extraction failed: {str(e)}")
            return []
    
    def _validate_customer_input(self, user_input: str, customer_name: str) -> dict:
        """Validate customer ID or phone number input"""
        
        validation_task = Task(
            description=f"""Validate this customer input and determine the search strategy:

USER INPUT: "{user_input}"
CUSTOMER NAME FROM QUESTION: "{customer_name}"

VALIDATION RULES:
1. Customer ID: Must be exactly 11 digits (numbers or characters)
2. Phone Number: Must be 8-11 digits (all numbers)
3. Company ID: Business registration format

Your task:
1. Identify if the input is a Customer ID, Phone Number, or Company ID
2. Validate the format according to business rules
3. Recommend the database search strategy

Return JSON format:
{{"input_type": "CUSTOMER_ID/PHONE/COMPANY_ID", "is_valid": true/false, "search_field": "CUST_ID_NO/phone_field/COMP_EID_NO", "formatted_input": "cleaned_input", "validation_message": "explanation"}}""",
            expected_output="Input validation results in JSON format",
            agent=self.customer_validator.get_agent()
        )
        
        crew = Crew(agents=[self.customer_validator.get_agent()], tasks=[validation_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            import re
            
            # Extract JSON from markdown code blocks if present
            result_clean = result.strip()
            
            # Look for JSON wrapped in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', result_clean, re.DOTALL | re.IGNORECASE)
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # Look for JSON wrapped in plain code blocks
                code_match = re.search(r'```\s*(.*?)\s*```', result_clean, re.DOTALL)
                if code_match:
                    json_content = code_match.group(1).strip()
                else:
                    # No code blocks, use raw result
                    json_content = result_clean
            
            # Try to find JSON-like structure if above methods fail
            if not json_content.strip().startswith('{'):
                # Look for JSON object pattern anywhere in the text
                json_pattern = re.search(r'\{.*\}', result_clean, re.DOTALL)
                if json_pattern:
                    json_content = json_pattern.group(0)
                else:
                    json_content = result_clean
            
            validation_result = js.loads(json_content)
            
            if validation_result['is_valid']:
                # Search for customer in database
                search_result = self._search_customer_in_database(
                    validation_result['formatted_input'], 
                    validation_result['input_type'],
                    customer_name
                )
                
                if search_result['status'] == 'found':
                    return {
                        'status': 'valid',
                        'customer_data': search_result['customers'],
                        'search_type': validation_result['input_type'],
                        'proceed': True
                    }
                elif search_result['status'] == 'multiple':
                    return {
                        'status': 'multiple_matches',
                        'customers': search_result['customers'],
                        'search_type': validation_result['input_type'],
                        'original_name': customer_name
                    }
                else:
                    return {
                        'status': 'invalid',
                        'message': f"No customer found with {validation_result['input_type']}: {user_input}"
                    }
            else:
                return {
                    'status': 'invalid',
                    'message': validation_result['validation_message']
                }
                
        except Exception as e:
            print(f"⚠️ Customer validation failed: {str(e)}")
            return {
                'status': 'invalid',
                'message': f"Validation failed: {str(e)}"
            }
    
    def _search_customer_in_database(self, search_value: str, search_type: str, customer_name: str) -> dict:
        """Search for customer in database using appropriate field"""
        try:
            if search_type == 'CUSTOMER_ID':
                search_field = 'CUST_ID_NO'
                query = f"SELECT DISTINCT DOC_CUST_NAME, CUST_ID_NO, COMP_EID_NO FROM insmv.AIMS_ALL_DATA WHERE CUST_ID_NO = '{search_value}'"
            elif search_type == 'PHONE':
                # Search multiple phone fields
                query = f"""SELECT DISTINCT DOC_CUST_NAME, CUST_ID_NO, COMP_EID_NO 
                           FROM insmv.AIMS_ALL_DATA 
                           WHERE (CUST_PHONE_NO LIKE '%{search_value}%' 
                               OR CUST_MOBILE_NO LIKE '%{search_value}%')"""
            elif search_type == 'COMPANY_ID':
                search_field = 'COMP_EID_NO'
                query = f"SELECT DISTINCT DOC_CUST_NAME, CUST_ID_NO, COMP_EID_NO FROM insmv.AIMS_ALL_DATA WHERE COMP_EID_NO = '{search_value}'"
            else:
                return {'status': 'error', 'message': 'Unknown search type'}
            
            results = self.db_utils._safe_execute_query(query)
            
            if len(results) == 0:
                return {'status': 'not_found'}
            elif len(results) == 1:
                return {'status': 'found', 'customers': results.to_dict('records')}
            else:
                return {'status': 'multiple', 'customers': results.to_dict('records')}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _handle_multiple_customer_matches(self, validation_result: dict, customer_name: str, user_question: str) -> dict:
        """Handle cases where multiple customers match the phone number"""
        customers = validation_result['customers']
        
        print(f"\n📋 Found {len(customers)} customers with the provided information:")
        print("🔍 Please select the correct customer:")
        
        for i, customer in enumerate(customers, 1):
            cust_name = customer.get('DOC_CUST_NAME', 'Unknown')
            cust_id = customer.get('CUST_ID_NO', 'N/A')
            comp_id = customer.get('COMP_EID_NO', 'N/A')
            
            if cust_id and cust_id != 'N/A':
                print(f"{i}. {cust_name} (Individual - ID: {cust_id})")
            elif comp_id and comp_id != 'N/A':
                print(f"{i}. {cust_name} (Company - ID: {comp_id})")
            else:
                print(f"{i}. {cust_name}")
        
        while True:
            try:
                choice = input(f"\n🎯 Select customer (1-{len(customers)}) or type the customer name: ").strip()
                
                # Check if user entered a number
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(customers):
                        selected_customer = customers[choice_num - 1]
                        print(f"✅ Selected: {selected_customer['DOC_CUST_NAME']}")
                        return {
                            'status': 'valid',
                            'customer_data': [selected_customer],
                            'search_type': validation_result['search_type'],
                            'proceed': True
                        }
                    else:
                        print(f"❌ Please enter a number between 1 and {len(customers)}")
                        continue
                except ValueError:
                    # User entered text, try intelligent name matching
                    match_result = self._intelligent_name_matching(choice, customers, customer_name)
                    if match_result['status'] == 'match_found':
                        return {
                            'status': 'valid',
                            'customer_data': [match_result['customer']],
                            'search_type': validation_result['search_type'],
                            'proceed': True
                        }
                    else:
                        print(f"❌ {match_result['message']}")
                        continue
                        
            except KeyboardInterrupt:
                return {'status': 'cancelled', 'proceed': False}
    
    def _evaluate_and_decide(self, execution_result: dict, user_question: str, cycle: int) -> dict:
        """PHASE 3: Results Evaluation & Decision Making"""
        print("🤔 PHASE 3: Results Evaluation & Decision Making")
        
        # Add domain knowledge context for evaluation
        domain_context = format_domain_knowledge_for_planning(self.domain_knowledge, user_question)
        
        evaluation_task = Task(
            description=f"""As the Results Intelligence Evaluator, analyze these query results using comprehensive AIMS business knowledge:

USER QUESTION: {user_question}
CYCLE: {cycle}
EXECUTION RESULTS: {execution_result}

{get_comprehensive_aims_knowledge_summary()}

EVALUATION CONTEXT:
{domain_context}

BE DECISIVE AND EFFICIENT - Evaluate quickly:

QUICK COMPLETENESS CHECK:
1. Does the data directly answer what the user asked?
2. Are the key data points present and relevant?
3. If calculations were needed, were they performed correctly?
4. Is there enough information for the user to understand the answer?

DECISION MATRIX (Choose COMPLETE when possible):
- User asked for policies → Got policies with relevant details = COMPLETE
- User asked for claims → Got claims with amounts/status = COMPLETE
- User asked for calculations → Got correct calculations = COMPLETE
- User asked for comparisons → Got data from all compared items = COMPLETE
- User asked broad question → Got representative sample = COMPLETE

ONLY choose CONTINUE if:
- Critical data is obviously missing (e.g., asked for amounts but got none)
- Calculation is clearly wrong or incomplete
- Question has multiple parts and only one part was answered

ONLY choose ASK_USER if:
- Results are completely unrelated to question
- Question is genuinely ambiguous

DEFAULT TO COMPLETE: When in doubt, favor COMPLETE over CONTINUE.

Respond with JSON:
{{"status": "COMPLETE/CONTINUE/ASK_USER", "confidence": 0.9, "rationale": "...", "summary": "..."}}""",
            expected_output="Evaluation results in JSON format",
            agent=self.results_evaluator.get_agent()
        )
        
        crew = Crew(agents=[self.results_evaluator.get_agent()], tasks=[evaluation_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            return js.loads(result.strip())
        except:
            return {"status": "CONTINUE", "confidence": 0.5, "rationale": result}
    
    def _intelligent_name_matching(self, user_input: str, available_customers: list, original_name: str) -> dict:
        """Use AI agent to intelligently match user input with available customer names"""
        
        customer_names = [customer.get('DOC_CUST_NAME', '') for customer in available_customers]
        
        matching_task = Task(
            description=f"""Match user input with available customer names using intelligent comparison:

USER INPUT: "{user_input}"
ORIGINAL NAME FROM QUESTION: "{original_name}"
AVAILABLE CUSTOMERS: {customer_names}

Your task:
1. Find the best match for the user input among available customers
2. Consider exact matches, partial matches, and fuzzy matching
3. Account for spelling variations and nicknames
4. Consider the context of the original name from the question

MATCHING STRATEGIES:
- Exact match gets highest priority
- Substring matches for partial names
- Case-insensitive comparison  
- Common spelling variations
- Cultural name variations (Arabic/English)

Return JSON format:
{{"status": "match_found/no_match/ambiguous", "matched_name": "exact_name_from_list", "confidence": 0.95, "reasoning": "why_this_match_was_chosen"}}""",
            expected_output="Name matching results in JSON format",  
            agent=self.name_matcher.get_agent()
        )
        
        crew = Crew(agents=[self.name_matcher.get_agent()], tasks=[matching_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            import re
            
            # Extract JSON from markdown code blocks if present
            result_clean = result.strip()
            
            # Look for JSON wrapped in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', result_clean, re.DOTALL | re.IGNORECASE)
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # Look for JSON wrapped in plain code blocks
                code_match = re.search(r'```\s*(.*?)\s*```', result_clean, re.DOTALL)
                if code_match:
                    json_content = code_match.group(1).strip()
                else:
                    # No code blocks, use raw result
                    json_content = result_clean
            
            # Try to find JSON-like structure if above methods fail
            if not json_content.strip().startswith('{'):
                # Look for JSON object pattern anywhere in the text
                json_pattern = re.search(r'\{.*\}', result_clean, re.DOTALL)
                if json_pattern:
                    json_content = json_pattern.group(0)
                else:
                    json_content = result_clean
            
            match_result = js.loads(json_content)
            
            if match_result['status'] == 'match_found':
                # Find the customer object that matches
                matched_name = match_result['matched_name']
                for customer in available_customers:
                    if customer.get('DOC_CUST_NAME', '') == matched_name:
                        return {
                            'status': 'match_found',
                            'customer': customer,
                            'confidence': match_result['confidence']
                        }
                
                return {'status': 'error', 'message': 'Matched name not found in customer list'}
            else:
                return {
                    'status': 'no_match',
                    'message': f"Could not find a good match for '{user_input}' among available customers"
                }
                
        except Exception as e:
            print(f"⚠️ JSON parsing failed for name matching: {str(e)}")
            return {'status': 'error', 'message': f"Name matching failed: {str(e)}"}
    
    def _get_all_broker_names(self, branch_filter: list = None) -> list:
        """Retrieve unique broker names from DOC_AGENT_NAME field, optionally filtered by branch"""
        try:
            # Build base query
            query = """
                SELECT DISTINCT DOC_AGENT_NAME 
                FROM insmv.AIMS_ALL_DATA 
                WHERE DOC_AGENT_NAME IS NOT NULL 
            """
            
            # Add branch filtering if specified
            if branch_filter and len(branch_filter) > 0:
                branch_conditions = []
                for branch in branch_filter:
                    branch_conditions.append(f"UPPER(DOC_BRANCH_NAME) LIKE UPPER('%{branch}%')")
                
                branch_filter_clause = " OR ".join(branch_conditions)
                query += f" AND ({branch_filter_clause})"
                print(f"🔍 Filtering brokers by branch(es): {', '.join(branch_filter)}")
            
            results = self.db_utils._safe_execute_query(query)
            
            if len(results) > 0:
                broker_names = results['DOC_AGENT_NAME'].dropna().unique().tolist()
                # Clean up names - remove empty strings and None values
                broker_names = [name.strip() for name in broker_names if name and str(name).strip() != '' and str(name).lower() != 'nan']
                return broker_names
            else:
                branch_msg = f" in branch(es) {', '.join(branch_filter)}" if branch_filter else ""
                print(f"⚠️ No broker names found in database{branch_msg}")
                return []
                
        except Exception as e:
            print(f"❌ Error retrieving broker names: {str(e)}")
            return []
    
    def _intelligent_broker_matching(self, user_input: str, available_brokers: list) -> dict:
        """Use AI agent to intelligently match user input with available broker names"""
        
        # Limit the list to prevent overwhelming the AI
        broker_sample = available_brokers  # Top 100 brokers for matching
        
        matching_task = Task(
            description=f"""Match user input with available broker names using intelligent comparison:

USER INPUT: "{user_input}"
AVAILABLE BROKERS (sample): {broker_sample}
TOTAL BROKERS IN DATABASE: {len(available_brokers)}

Your task:
1. Find the best matches for the user input among available brokers
2. Consider exact matches, partial matches, and fuzzy matching
3. Account for spelling variations, nicknames, and cultural variations
4. Handle common Arabic/English name transliterations
5. Rank matches by confidence

MATCHING STRATEGIES:
- Exact match gets highest priority (confidence 1.0)
- Partial name matches (first name, last name, substring)
- Case-insensitive comparison
- Common spelling variations and nicknames
- Cultural name variations (Arabic/English transliterations)
- Phonetic similarity for pronunciation-based matches

RESPONSE RULES:
- If 1 exact match: Return "exact_match" with the broker name
- If 2-10 good matches: Return "multiple_matches" with list of matches
- If >10 matches: Return top 10 best matches as "multiple_matches"
- If no good matches: Return "no_match"

Return JSON format:
{{"status": "exact_match/multiple_matches/no_match", "matches": ["broker1", "broker2"], "confidence_scores": [0.95, 0.85], "reasoning": "explanation"}}

For exact_match, also include: "broker": "exact_broker_name"
""",
            expected_output="Broker matching results in JSON format",  
            agent=self.name_matcher.get_agent()
        )
        
        crew = Crew(agents=[self.name_matcher.get_agent()], tasks=[matching_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            import re
            
            # Extract JSON from markdown code blocks if present
            result_clean = result.strip()
            
            # Look for JSON wrapped in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', result_clean, re.DOTALL | re.IGNORECASE)
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # Look for JSON wrapped in plain code blocks
                code_match = re.search(r'```\s*(.*?)\s*```', result_clean, re.DOTALL)
                if code_match:
                    json_content = code_match.group(1).strip()
                else:
                    # No code blocks, use raw result
                    json_content = result_clean
            
            # Try to find JSON-like structure if above methods fail
            if not json_content.strip().startswith('{'):
                # Look for JSON object pattern anywhere in the text
                json_pattern = re.search(r'\{.*\}', result_clean, re.DOTALL)
                if json_pattern:
                    json_content = json_pattern.group(0)
                else:
                    json_content = result_clean
            
            match_result = js.loads(json_content)
            
            return match_result
            
        except Exception as e:
            print(f"⚠️ JSON parsing failed for broker matching: {str(e)}")
            return {'status': 'no_match', 'message': f"Broker matching failed: {str(e)}"}
    
    def _handle_multiple_broker_matches(self, match_result: dict, agent_name: str, user_question: str) -> dict:
        """Handle cases where multiple brokers match the input name"""
        brokers = match_result.get('matches', [])
        confidence_scores = match_result.get('confidence_scores', [])
        
        print(f"\n📋 Found {len(brokers)} broker matches for '{agent_name}':")
        print("🔍 Please select the correct broker:")
        
        # Display matches with confidence scores if available
        for i, broker in enumerate(brokers, 1):
            confidence = confidence_scores[i-1] if i-1 < len(confidence_scores) else 0.0
            if confidence > 0:
                print(f"{i}. {broker} (confidence: {confidence:.2f})")
            else:
                print(f"{i}. {broker}")
        
        while True:
            try:
                choice = input(f"\n🎯 Select broker (1-{len(brokers)}) or type the broker name: ").strip()
                
                # Check if user entered a number
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(brokers):
                        selected_broker = brokers[choice_num - 1]
                        print(f"✅ Selected: {selected_broker}")
                        return {
                            'status': 'valid',
                            'broker_name': selected_broker,
                            'search_type': 'AGENT_NAME',
                            'proceed': True
                        }
                    else:
                        print(f"❌ Please enter a number between 1 and {len(brokers)}")
                        continue
                except ValueError:
                    # User entered text, try to match with the provided options
                    user_choice_lower = choice.lower()
                    matched_broker = None
                    
                    # Try exact match first
                    for broker in brokers:
                        if broker.lower() == user_choice_lower:
                            matched_broker = broker
                            break
                    
                    # Try partial match if exact match fails
                    if not matched_broker:
                        for broker in brokers:
                            if user_choice_lower in broker.lower() or broker.lower() in user_choice_lower:
                                matched_broker = broker
                                break
                    
                    if matched_broker:
                        print(f"✅ Selected: {matched_broker}")
                        return {
                            'status': 'valid',
                            'broker_name': matched_broker,
                            'search_type': 'AGENT_NAME',
                            'proceed': True
                        }
                    else:
                        print(f"❌ '{choice}' doesn't match any of the provided options. Please try again.")
                        continue
                        
            except KeyboardInterrupt:
                return {'status': 'cancelled', 'proceed': False}
    
    def _evaluate_and_decide(self, execution_result: dict, user_question: str, cycle: int) -> dict:
        """PHASE 3: Results Evaluation & Decision Making"""
        print("🤔 PHASE 3: Results Evaluation & Decision Making")
        
        # Add domain knowledge context for evaluation
        domain_context = format_domain_knowledge_for_planning(self.domain_knowledge, user_question)
        
        evaluation_task = Task(
            description=f"""As the Results Intelligence Evaluator, analyze these query results using comprehensive AIMS business knowledge:

USER QUESTION: {user_question}
CYCLE: {cycle}
EXECUTION RESULTS: {execution_result}

{get_comprehensive_aims_knowledge_summary()}

EVALUATION CONTEXT:
{domain_context}

BE DECISIVE AND EFFICIENT - Evaluate quickly:

QUICK COMPLETENESS CHECK:
1. Does the data directly answer what the user asked?
2. Are the key data points present and relevant?
3. If calculations were needed, were they performed correctly?
4. Is there enough information for the user to understand the answer?

DECISION MATRIX (Choose COMPLETE when possible):
- User asked for policies → Got policies with relevant details = COMPLETE
- User asked for claims → Got claims with amounts/status = COMPLETE
- User asked for calculations → Got correct calculations = COMPLETE
- User asked for comparisons → Got data from all compared items = COMPLETE
- User asked broad question → Got representative sample = COMPLETE

ONLY choose CONTINUE if:
- Critical data is obviously missing (e.g., asked for amounts but got none)
- Calculation is clearly wrong or incomplete
- Question has multiple parts and only one part was answered

ONLY choose ASK_USER if:
- Results are completely unrelated to question
- Question is genuinely ambiguous

DEFAULT TO COMPLETE: When in doubt, favor COMPLETE over CONTINUE.

Respond with JSON:
{{"status": "COMPLETE/CONTINUE/ASK_USER", "confidence": 0.9, "rationale": "...", "summary": "..."}}""",
            expected_output="Evaluation results in JSON format",
            agent=self.results_evaluator.get_agent()
        )
        
        crew = Crew(agents=[self.results_evaluator.get_agent()], tasks=[evaluation_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            return js.loads(result.strip())
        except:
            return {"status": "CONTINUE", "confidence": 0.5, "rationale": result}
    
    def _get_all_user_names(self, branch_filter: list = None) -> list:
        """Retrieve unique user names from DOC_USER_NAME field, optionally filtered by branch"""
        try:
            # Build base query
            query = """
                SELECT DISTINCT DOC_USER_NAME 
                FROM insmv.AIMS_ALL_DATA 
                WHERE DOC_USER_NAME IS NOT NULL 
            """
            
            # Add branch filtering if specified
            if branch_filter and len(branch_filter) > 0:
                branch_conditions = []
                for branch in branch_filter:
                    branch_conditions.append(f"UPPER(DOC_BRANCH_NAME) LIKE UPPER('%{branch}%')")
                
                branch_filter_clause = " OR ".join(branch_conditions)
                query += f" AND ({branch_filter_clause})"
                print(f"🔍 Filtering users by branch(es): {', '.join(branch_filter)}")
            
            results = self.db_utils._safe_execute_query(query)
            
            if len(results) > 0:
                user_names = results['DOC_USER_NAME'].dropna().unique().tolist()
                # Clean up names - remove empty strings and None values
                user_names = [name.strip() for name in user_names if name and str(name).strip() != '' and str(name).lower() != 'nan']
                return user_names
            else:
                branch_msg = f" in branch(es) {', '.join(branch_filter)}" if branch_filter else ""
                print(f"⚠️ No system user names found in database{branch_msg}")
                return []
                
        except Exception as e:
            print(f"❌ Error retrieving user names: {str(e)}")
            return []
    
    def _intelligent_user_matching(self, user_input: str, available_users: list) -> dict:
        """Use AI agent to intelligently match user input with available system user names"""
        
        # Use the same name matcher agent for users
        matching_task = Task(
            description=f"""Match user input with available system user names using intelligent comparison:

USER INPUT: "{user_input}"
AVAILABLE USERS: {available_users}
TOTAL USERS IN DATABASE: {len(available_users)}

Your task:
1. Find the best matches for the user input among available system users
2. Consider exact matches, partial matches, and fuzzy matching
3. Account for spelling variations, nicknames, and cultural variations
4. Handle common Arabic/English name transliterations
5. Rank matches by confidence

MATCHING STRATEGIES:
- Exact match gets highest priority (confidence 1.0)
- Partial name matches (first name, last name, substring)
- Case-insensitive comparison
- Common spelling variations and nicknames
- Cultural name variations (Arabic/English transliterations)
- Phonetic similarity for pronunciation-based matches

RESPONSE RULES:
- If 1 exact match: Return "exact_match" with the user name
- If 2-10 good matches: Return "multiple_matches" with list of matches
- If >10 matches: Return top 10 best matches as "multiple_matches"
- If no good matches: Return "no_match"

Return JSON format:
{{"status": "exact_match/multiple_matches/no_match", "matches": ["user1", "user2"], "confidence_scores": [0.95, 0.85], "reasoning": "explanation"}}

For exact_match, also include: "user": "exact_user_name"
""",
            expected_output="User matching results in JSON format",  
            agent=self.name_matcher.get_agent()
        )
        
        crew = Crew(agents=[self.name_matcher.get_agent()], tasks=[matching_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            import re
            
            # Extract JSON from markdown code blocks if present
            result_clean = result.strip()
            
            # Look for JSON wrapped in markdown code blocks
            json_match = re.search(r'```json\s*(.*?)\s*```', result_clean, re.DOTALL | re.IGNORECASE)
            if json_match:
                json_content = json_match.group(1).strip()
            else:
                # Look for JSON wrapped in plain code blocks
                code_match = re.search(r'```\s*(.*?)\s*```', result_clean, re.DOTALL)
                if code_match:
                    json_content = code_match.group(1).strip()
                else:
                    # No code blocks, use raw result
                    json_content = result_clean
            
            # Try to find JSON-like structure if above methods fail
            if not json_content.strip().startswith('{'):
                # Look for JSON object pattern anywhere in the text
                json_pattern = re.search(r'\{.*\}', result_clean, re.DOTALL)
                if json_pattern:
                    json_content = json_pattern.group(0)
                else:
                    json_content = result_clean
            
            match_result = js.loads(json_content)
            
            return match_result
            
        except Exception as e:
            print(f"⚠️ JSON parsing failed for user matching: {str(e)}")
            return {'status': 'no_match', 'message': f"User matching failed: {str(e)}"}
    
    def _handle_multiple_user_matches(self, match_result: dict, user_name: str, user_question: str) -> dict:
        """Handle cases where multiple system users match the input name"""
        users = match_result.get('matches', [])
        confidence_scores = match_result.get('confidence_scores', [])
        
        print(f"\n📋 Found {len(users)} system user matches for '{user_name}':")
        print("🔍 Please select the correct system user:")
        
        # Display matches with confidence scores if available
        for i, user in enumerate(users, 1):
            confidence = confidence_scores[i-1] if i-1 < len(confidence_scores) else 0.0
            if confidence > 0:
                print(f"{i}. {user} (confidence: {confidence:.2f})")
            else:
                print(f"{i}. {user}")
        
        while True:
            try:
                choice = input(f"\n🎯 Select system user (1-{len(users)}) or type the user name: ").strip()
                
                # Check if user entered a number
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(users):
                        selected_user = users[choice_num - 1]
                        print(f"✅ Selected: {selected_user}")
                        return {
                            'status': 'valid',
                            'user_name': selected_user,
                            'search_type': 'USER_NAME',
                            'proceed': True
                        }
                    else:
                        print(f"❌ Please enter a number between 1 and {len(users)}")
                        continue
                except ValueError:
                    # User entered text, try to match with the provided options
                    user_choice_lower = choice.lower()
                    matched_user = None
                    
                    # Try exact match first
                    for user in users:
                        if user.lower() == user_choice_lower:
                            matched_user = user
                            break
                    
                    # Try partial match if exact match fails
                    if not matched_user:
                        for user in users:
                            if user_choice_lower in user.lower() or user.lower() in user_choice_lower:
                                matched_user = user
                                break
                    
                    if matched_user:
                        print(f"✅ Selected: {matched_user}")
                        return {
                            'status': 'valid',
                            'user_name': matched_user,
                            'search_type': 'USER_NAME',
                            'proceed': True
                        }
                    else:
                        print(f"❌ '{choice}' doesn't match any of the provided options. Please try again.")
                        continue
                        
            except KeyboardInterrupt:
                return {'status': 'cancelled', 'proceed': False}
    
    def _evaluate_and_decide(self, execution_result: dict, user_question: str, cycle: int) -> dict:
        """PHASE 3: Results Evaluation & Decision Making"""
        print("🤔 PHASE 3: Results Evaluation & Decision Making")
        
        # Add domain knowledge context for evaluation
        domain_context = format_domain_knowledge_for_planning(self.domain_knowledge, user_question)
        
        evaluation_task = Task(
            description=f"""As the Results Intelligence Evaluator, analyze these query results using comprehensive AIMS business knowledge:

USER QUESTION: {user_question}
CYCLE: {cycle}
EXECUTION RESULTS: {execution_result}

{get_comprehensive_aims_knowledge_summary()}

EVALUATION CONTEXT:
{domain_context}

BE DECISIVE AND EFFICIENT - Evaluate quickly:

QUICK COMPLETENESS CHECK:
1. Does the data directly answer what the user asked?
2. Are the key data points present and relevant?
3. If calculations were needed, were they performed correctly?
4. Is there enough information for the user to understand the answer?

DECISION MATRIX (Choose COMPLETE when possible):
- User asked for policies → Got policies with relevant details = COMPLETE
- User asked for claims → Got claims with amounts/status = COMPLETE
- User asked for calculations → Got correct calculations = COMPLETE
- User asked for comparisons → Got data from all compared items = COMPLETE
- User asked broad question → Got representative sample = COMPLETE

ONLY choose CONTINUE if:
- Critical data is obviously missing (e.g., asked for amounts but got none)
- Calculation is clearly wrong or incomplete
- Question has multiple parts and only one part was answered

ONLY choose ASK_USER if:
- Results are completely unrelated to question
- Question is genuinely ambiguous

DEFAULT TO COMPLETE: When in doubt, favor COMPLETE over CONTINUE.

Respond with JSON:
{{"status": "COMPLETE/CONTINUE/ASK_USER", "confidence": 0.9, "rationale": "...", "summary": "..."}}""",
            expected_output="Evaluation results in JSON format",
            agent=self.results_evaluator.get_agent()
        )
        
        crew = Crew(agents=[self.results_evaluator.get_agent()], tasks=[evaluation_task], process=Process.sequential, memory=False)
        result = str(crew.kickoff())
        
        try:
            import json as js
            return js.loads(result.strip())
        except:
            return {"status": "CONTINUE", "confidence": 0.5, "rationale": result}
