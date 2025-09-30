"""
Context builder utilities for AI agents
"""


def get_comprehensive_aims_knowledge_summary() -> str:
    """Get a comprehensive summary of AIMS database knowledge for agent tasks"""
    return f"""
=== COMPREHENSIVE AIMS DATABASE KNOWLEDGE ===

BUSINESS OVERVIEW:
Insurance management system with 200+ fields covering policies, claims, payments, and reinsurance.
Multi-national insurance company with 5 branches, 32 offices, and 9 lines of business operations.

ORGANIZATIONAL STRUCTURE:
• 5 Main Branches: Main Branch (21 offices), Doha Islamic - Shamel (8 Takaful offices), India Branch (1), Mena Life (1), Mena Re Underwriters (1)
• 32 Total Offices across Qatar, India, Lebanon, and Dubai
• 9 Lines of Business: Motor, Group Life & Medical, Fire, General Accident, Marine Cargo, Marine Hull, Aviation, Energy, Engineering
• 4 Distribution Channel Types: Digital (WEB, Online agents, Call Center), Retail (Lulu Centers), Partnerships (Qatar Energy, Hamad Airport), Specialized operations
• International Presence: Qatar (main operations), India (IFSC), Lebanon (Mena Life), Dubai (Mena Re)

KEY STATISTICS:
• 628 vehicle makes, 6,962 models, 251 body types
• 5 claim branches, 31 claim offices, 32 total offices
• 43 accident types (majority: Material damage to third party vehicle)
• 18 plate types, 15 cylinder types, 5 plate colors
• 11 data sources (Mobile App, Agent/Broker, Web, Call Center, etc.)
• 8 premium periods for financial breakdown

CRITICAL BUSINESS RULES:
• Policy Key: branch + office + class + subclass + pol_no + pol_year
• CRITICAL DUAL COUNTING: For policy count questions, provide BOTH values:
  - POLICY COUNT: COUNT(DISTINCT CASE WHEN DOC_TYPE IN (1,4) THEN DOC_KEY_FORM END)
  - TRANSACTION COUNT: COUNT(DISTINCT DOC_KEY_FORM)
• DOC_KEY_FORM: Unique document identifier - THE field for all counting operations
• DOC_TYPE Values: 1=New Policy, 4=Renewal Policy (actual policies), Others=Amendments/Cancellations/etc (transactions)
• Claim Key: CLAIM_BRANCH + CLAIM_OFFICE + class + subclass + CLAIM_NO + CLAIM_ACC_YEAR
• Payment Key: claim_key + PAY_SLIP_NO + PAY_SLIP_YEAR
• Open Claims: CLAIM_CLOSE_DT IS NULL
• CUSTOMER ID DISTINCTION: CUST_ID_NO (National ID - primary) vs DOC_CUST_SL_COD1 (customer code - different field)
• BUSINESS CHANNEL CLASSIFICATION: DOC_AGENT_NAME NULL = DIRECT business, NOT NULL = BROKER business
• Individual Customers: CUST_ID_NO not null, COMP_EID_NO null
• Company Customers: CUST_ID_NO null, COMP_EID_NO not null
• Active Policies: DOC_ST_DT <= CURRENT_DATE AND DOC_INS_ED_DT >= CURRENT_DATE
• CRITICAL: PREMIUM ≠ GROSS WRITTEN PREMIUM (Different concepts!)
  - Basic Premium: Use DOC_PREMIUM field for general "premium" queries
  - Gross Written Premium: Use calculation ONLY when specifically requested (gross, GWP, gross premium)
• Loss Ratio: Use SQL template - SELECT (( SUM(COALESCE(T.PAY_AMT, 0)) + SUM(COALESCE(T.CLAIM_OS_VAL, 0)) - SUM(COALESCE(T.PAY_REC_AMT, 0)) ) / NULLIF(SUM(COALESCE(T.DOC_PREMIUM, 0)), 0)) * 100 AS LOSS_RATIO FROM insmv.AIMS_ALL_DATA T (modify based on requirements)
• Gross Written Premium (ONLY when specifically requested): Use SQL template - SELECT (COALESCE(T.DOC_PREMIUM, 0) + COALESCE(T.PRD_FEES4L, 0) - COALESCE(T.PRD_NPREM7L, 0) - COALESCE(T.PRD_NPREM8L, 0)) AS GROSS_WRITTEN_PREMIUM FROM insmv.AIMS_ALL_DATA T

CRITICAL SEARCH KEY PATTERNS:
• Claim Search: claim branch + claim office + maj type + min type + claim no + claim acc year
• Policy Search: branch + office + maj type + min type + policy number + policy year
• Customer Search - SPECIFIC CUSTOMER: Use CUST_ID_NO (National ID - primary), COMP_EID_NO (companies), DOC_CUST_NAME (name), or phone fields
• IMPORTANT: CUST_ID_NO ≠ DOC_CUST_SL_COD1 (CUST_ID_NO is National ID, DOC_CUST_SL_COD1 is customer code)
• Customer Search - COUNTING/STATISTICS: Use DOC_CUST_SL_COD1 for aggregate queries if needed (but CUST_ID_NO is primary)
• Key Fields for Claims: CLAIM_BRANCH + CLAIM_OFFICE + DOC_MAJ_INS_TYPE + DOC_MIN_INS_TYPE + CLAIM_NO + CLAIM_ACC_YEAR
• Key Fields for Policies: DOC_BRANCH + DOC_OFFICE + DOC_MAJ_INS_TYPE + DOC_MIN_INS_TYPE + POL_NO + POL_YEAR
• Best Practice: Always use complete keys for accurate searches - partial keys may return multiple matches

CRITICAL FIELD NAMING CONVENTIONS:
• Pattern: Fields ending with _TYPE contain codes (1, 2, 3), fields ending with _NAME contain descriptive text
• Code Fields (_TYPE): DOC_MAJ_INS_TYPE (29=Motor), DOC_MIN_INS_TYPE (111=Comp), CLAIM_ACC_TYPE (4=Material damage)
• Name Fields (_NAME): DOC_MAJ_NAME (Motor, Medical), DOC_MIN_NAME (Comprehensive), CLAIM_ACC_TYPE_NAME (descriptions)
• Usage: Use _NAME fields for user-friendly queries, _TYPE fields for precise code matching
• Best Practice: When user asks for 'Motor insurance', use DOC_MAJ_NAME = 'Motor' OR DOC_MAJ_INS_TYPE = 29
• ALTERNATIVE TERMINOLOGY: 
  - Major fields (DOC_MAJ_INS_TYPE/DOC_MAJ_NAME) also called: 'line of business', 'class', 'insurance line'
  - Minor fields (DOC_MIN_INS_TYPE/DOC_MIN_NAME) also called: 'product', 'subclass', 'product type'
  - When users say 'product', 'subclass' → use DOC_MIN_INS_TYPE or DOC_MIN_NAME
  - When users say 'line of business', 'class' → use DOC_MAJ_INS_TYPE or DOC_MAJ_NAME

CRITICAL DATE QUERY RULES:
• When user asks for policies "in [year]" (e.g., "policies in 2022"), use DOC_REG_DT, NOT POL_YEAR
• DOC_REG_DT = when policy was registered in system (what users typically mean)
• POL_YEAR = policy document year (use only when specifically asking about document year)
• Example: "find policies in 2022" → WHERE EXTRACT(YEAR FROM DOC_REG_DT) = 2022

ESSENTIAL FIELDS BY CATEGORY:
Policy: DOC_SERIAL, DOC_BRANCH, DOC_OFFICE, POL_NO, POL_YEAR, DOC_TYPE, DOC_ST_DT, DOC_INS_ED_DT, DOC_MAJ_INS_TYPE, DOC_MIN_INS_TYPE
Customer: DOC_CUST_NAME (name search), CUST_ID_NO (individual ID), COMP_EID_NO (company ID), CUST_NATIONALITY, ACCOUNT_STATUS, DOC_CUST_SD_COD1 (counting only)
Vehicle: DOC_PLATE_NO, DOC_MAKE_NAME, DOC_MODEL, DOC_PROD_YEAR, DOC_BODY_NAME, DOC_PLATE_TYPE_NAME
Financial: DOC_PREMIUM, DOC_SUM_INSURED, PRD_NPREMTL, PRD_PREMTL, DOC_COMM
Claims: CLAIM_BRANCH, CLAIM_OFFICE, CLAIM_NO, CLAIM_ACC_DT, CLAIM_CLOSE_DT, CLAIM_OS_VAL
Payments: PAY_SLIP_NO, PAY_AMT, PAY_REC_AMT, PAY_SLIP_TYPE_NAME, PAY_TP_LNAME
Dates: DOC_REG_DT (registration), DOC_ST_DT (start), DOC_INS_ED_DT (end), CLAIM_REG_DT, CLAIM_ACC_DT, PAY_SLIP_DT

DATA RELATIONSHIPS:
• One policy can have multiple claims
• One claim can have multiple payments  
• Policies link to claims via policy identification fields
• Claims link to payments via claim identification fields
• Financial data split across 8 premium periods
• Reinsurance has up to 5 facultative layers per policy
• Branches contain multiple offices with specific product lines
• Distribution channels serve different customer segments
• International operations provide regional coverage and specialized services
"""


def build_previous_results_context(intermediate_data: dict) -> str:
    """Build context from previous results for data flow"""
    if not intermediate_data:
        return ""
    
    previous_results_context = f"\nPREVIOUS STEP RESULTS:\n"
    for step_key, step_data in intermediate_data.items():
        if isinstance(step_data, dict) and 'results' in step_data:
            result_summary = f"- {step_key}: {len(step_data['results'])} rows"
            if len(step_data['results']) > 0:
                # Show ALL column names (no truncation)
                sample_row = step_data['results'][0] if step_data['results'] else {}
                result_summary += f", columns: {list(sample_row.keys())}"
            previous_results_context += result_summary + "\n"
    
    return previous_results_context
