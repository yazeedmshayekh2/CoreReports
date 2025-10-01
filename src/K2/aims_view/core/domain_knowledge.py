"""
AIMS Database Domain Knowledge
Contains comprehensive knowledge about the insurance database structure and business rules
"""


def load_aims_domain_knowledge():
    """Load comprehensive AIMS database domain knowledge from complete documentation"""
    return {
        # ======= ORGANIZATIONAL STRUCTURE =======
        "organizational_structure": {
            "total_branches": "5 main branches with specialized operations",
            "total_offices": "32 offices across all branches and countries",
            "branch_breakdown": {
                "Main Branch": "21 offices - Core operations, motor insurance, commercial lines",
                "Doha Islamic Insurance - Shamel": "8 offices - Takaful (Islamic insurance) operations", 
                "India Branch": "1 office - IFSC Branch, India (International operations)",
                "Mena Life": "1 office - Lebanon Mena Life (Life insurance operations)",
                "Mena Re Underwriters": "1 office - Dubai (Regional reinsurance hub)"
            },
            "main_branch_offices": [
                "Head Office", "Al-Khor", "Al-Rayyan", "Industrial Area", "Khalifa Office",
                "Old Airport", "Souq Waqif", "Lulu Barwa City", "Lulu D Ring", "Lulu Oasis",
                "Festival City", "Kiosk DIC", "CALL CENTER", "WEB", "Online_agent",
                "Hamad International Airport", "Qatar Energy", "Arab Orient", "DIC Agency",
                "Doha Mena Re", "Doha Warranties", "FAHES", "Al Ruwais"
            ],
            "takaful_offices": [
                "Doha Shamel Office", "Arab Orient (Doha Takaful)", "Mawater",
                "Al-Khor DT", "Qatar Energy_DT", "Shamel Agency", "Online_agent_DT", "WEB DT"
            ],
            "international_presence": "Qatar (main), India (IFSC), Lebanon (Mena Life), Dubai (Mena Re)",
            "distribution_channels": {
                "Digital": "WEB/WEB DT, Online agents, Call Center",
                "Retail": "3 Lulu Centers, Geographic offices",
                "Partnerships": "Qatar Energy, Hamad Airport, Arab Orient, Doha Warranties",
                "Specialized": "Head Office (commercial), Doha Mena Re (reinsurance)"
            }
        },
        
        "lines_of_business": {
            "Motor Insurance": {
                "branches": ["Doha Islamic Insurance - Shamel", "Main Branch"],
                "products": ["Comprehensive (Comp)", "Third Party Liability (T.P.L)", "Own Damage (O.D)", 
                           "Fleet Coverage", "Orange Card", "Personal Accident Benefits (P.A.B)"],
                "specialized": "Doha Warranties (Mercedes, Toyota, Mitsubishi, ISUZU brands)"
            },
            "GROUP LIFE & MEDICAL": {
                "branches": ["All branches except Mena Re Underwriters"],
                "products": ["Group Life", "Group Medical (DohaCare, IG, AY)", "Individual Medical",
                           "Travel Insurance", "Group Credit Life", "BUPA Plans", "Medical Reimbursement", 
                           "Domestic Helper coverage"]
            },
            "Fire Insurance": {
                "branches": ["Doha Islamic Insurance - Shamel", "India Branch", "Main Branch", "Mena Re Underwriters"],
                "products": ["Fire (Basic)", "Fire Consequential Loss", "Property All Risk", 
                           "Householders Comprehensive", "Fine Art", "Hoteliers Comprehensive",
                           "Sabotage & Terrorism", "Political Violence"]
            },
            "Marine Insurance": {
                "Marine Cargo": {
                    "branches": ["Doha Islamic Insurance - Shamel", "India Branch", "Main Branch", "Mena Re Underwriters"],
                    "products": ["Marine Cargo Open Cover", "Marine Cargo Individual Policy", 
                               "Marine Cargo Land Transit", "Freight Forwarders Liability"]
                },
                "Marine Hull": {
                    "branches": ["Doha Islamic Insurance - Shamel", "Main Branch"],
                    "products": ["Marine Hull & Liability", "Hull War", "Marine Liability (P+I)",
                               "Hull Pleasure Craft", "Builders Risks", "Ship Repairers Legal Liability",
                               "Port Terminal Authority Liability"]
                }
            },
            "Specialized Lines": {
                "Aviation": {
                    "branches": ["Doha Islamic Insurance - Shamel", "Main Branch"],
                    "products": ["Aviation Hull & Liability", "Aviation Hull Deductible", "Aviation Hull War",
                               "Aviation Liabilities", "Airport Authorities Operator Legal Liabilities"]
                },
                "Energy": {
                    "branches": ["India Branch", "Main Branch", "Mena Re Underwriters"],
                    "products": ["Contractors All Risk", "Property All Risk and Business Interruption",
                               "Energy Package Policy", "Sabotage and Terrorism", "Third Party Liability",
                               "Excess Operator's Extra Expense"]
                },
                "Engineering": {
                    "branches": ["Doha Islamic Insurance - Shamel", "Main Branch", "Mena Re Underwriters"],
                    "products": ["Contractors All Risks", "Contractors Plant & Machinery", "Electronic Equipment",
                               "Erection All Risks", "Machinery Breakdown", "Deterioration of Stocks",
                               "Machinery Loss of Profit"]
                }
            }
        },
        
        # ======= KEY BUSINESS RULES =======
        "business_rules": {
            "policy_key": "branch + office + class + subclass + pol_no + pol_year",
            "claim_key": "CLAIM_BRANCH + CLAIM_OFFICE + class + subclass + CLAIM_NO + CLAIM_ACC_YEAR",
            "payment_key": "claim_key + PAY_SLIP_NO + PAY_SLIP_YEAR",
            "policy_counting": {
                "rule": "For policy counting questions, provide BOTH policy count and transaction count",
                "field_to_count": "DOC_KEY_FORM",
                "policy_count": {
                    "filter": "DOC_TYPE IN (1, 4)",
                    "query": "SELECT COUNT(DISTINCT DOC_KEY_FORM) FROM table WHERE DOC_TYPE IN (1, 4)",
                    "description": "Actual policies only - new policies and renewals"
                },
                "transaction_count": {
                    "filter": "No DOC_TYPE filter (all types)",
                    "query": "SELECT COUNT(DISTINCT DOC_KEY_FORM) FROM table",
                    "description": "All document transactions - includes amendments, cancellations, endorsements, etc."
                },
                "doc_type_meanings": {
                    "1": "New Policy - Original policy issuance",
                    "4": "Renewal Policy - Policy renewal/continuation",
                    "others": "Amendments, cancellations, endorsements, etc."
                },
                "dual_count_query_template": "SELECT COUNT(DISTINCT CASE WHEN DOC_TYPE IN (1,4) THEN DOC_KEY_FORM END) as policy_count, COUNT(DISTINCT DOC_KEY_FORM) as transaction_count FROM insmv.AIMS_ALL_DATA [WHERE conditions]",
                "example_queries": {
                    "basic_count": "SELECT COUNT(DISTINCT CASE WHEN DOC_TYPE IN (1,4) THEN DOC_KEY_FORM END) as policy_count, COUNT(DISTINCT DOC_KEY_FORM) as transaction_count FROM insmv.AIMS_ALL_DATA",
                    "customer_count": "SELECT COUNT(DISTINCT CASE WHEN DOC_TYPE IN (1,4) THEN DOC_KEY_FORM END) as policy_count, COUNT(DISTINCT DOC_KEY_FORM) as transaction_count FROM insmv.AIMS_ALL_DATA WHERE CUST_ID_NO = 'customer_id'",
                    "agent_count": "SELECT COUNT(DISTINCT CASE WHEN DOC_TYPE IN (1,4) THEN DOC_KEY_FORM END) as policy_count, COUNT(DISTINCT DOC_KEY_FORM) as transaction_count FROM insmv.AIMS_ALL_DATA WHERE DOC_AGENT_NAME = 'agent_name'"
                },
                "response_format": "When providing counts, always explain both values clearly: 'Policy Count: X (actual insurance policies - new policies and renewals only), Transaction Count: Y (all document transactions including amendments, cancellations, etc.)'",
                "important_note": "ALWAYS provide both counts for policy counting questions - users need to understand the difference between actual policies and all transactions",
                "critical_reminder": "Policy count = business policies only, Transaction count = all document activity"
            },
            "customer_identification": {
                "primary_customer_id": "CUST_ID_NO",
                "customer_code": "DOC_CUST_SL_COD1", 
                "key_distinction": "CUST_ID_NO is the National ID for the customer (most commonly used), DOC_CUST_SL_COD1 is a separate customer code",
                "usage_priority": "CUST_ID_NO is the primary identifier - use this for customer searches and identification",
                "field_meanings": {
                    "CUST_ID_NO": "National ID of the customer - primary identifier for individuals",
                    "DOC_CUST_SL_COD1": "Customer code - internal system code, different from National ID"
                },
                "terminology_note": "'Customer code' and 'insured number' refer to the same concept - both are terms used for DOC_CUST_SL_COD1",
                "important_note": "These are two completely different fields - do not confuse or substitute one for the other"
            },
            "agent_broker_business": {
                "direct_business_rule": "When DOC_AGENT_NAME is NULL, it means DIRECT business (sold directly by the company)",
                "broker_business_rule": "When DOC_AGENT_NAME has a value, it means BROKER/AGENT business (sold through intermediary)",
                "business_classification": {
                    "direct": "DOC_AGENT_NAME IS NULL - Company direct sales",
                    "broker": "DOC_AGENT_NAME IS NOT NULL - Through broker/agent"
                },
                "important_note": "This distinction is crucial for business analysis and commission calculations"
            },
            "loss_ratio_formula": {
                "formula": "(Total PAY_AMT / Total Premium) * 100",
                "total_pay_amt_calculation": "(PAY_AMT + OS) - (PAY_REC_AMT)",
                "components": {
                    "PAY_AMT": "Payment amount (claims paid)",
                    "OS": "Outstanding amount (CLAIM_OS_VAL)", 
                    "PAY_REC_AMT": "Payment recovery amount (recoveries)",
                    "Premium": "DOC_PREMIUM (well known field)"
                },
                "business_logic": "Loss ratio shows claims expense vs premium income as percentage",
                "sql_template": """SELECT 
    (
        (
            SUM(COALESCE(T.PAY_AMT, 0)) 
            + SUM(COALESCE(T.CLAIM_OS_VAL, 0)) 
            - SUM(COALESCE(T.PAY_REC_AMT, 0))
        ) / NULLIF(SUM(COALESCE(T.DOC_PREMIUM, 0)), 0)
    ) * 100 AS LOSS_RATIO
FROM 
    insmv.AIMS_ALL_DATA T""",
                "sql_usage_notes": "Base template - add WHERE clauses, GROUP BY, and additional SELECT fields based on user's specific requirements"
            },
            "premium_terminology_distinctions": {
                "basic_premium": {
                    "field": "DOC_PREMIUM",
                    "description": "Base premium amount charged to customer - the standard policy premium",
                    "when_to_use": "When user asks for 'premium', 'policy premium', 'premium amount', or basic premium information",
                    "sql_example": "SELECT DOC_PREMIUM FROM insmv.AIMS_ALL_DATA T WHERE ..."
                },
                "gross_written_premium": {
                    "formula": "DOC_PREMIUM + PRD_FEES4L - PRD_NPREM7L - PRD_NPREM8L",
                    "description": "Calculated field including base premium plus fees and period adjustments",
                    "when_to_use": "ONLY when user specifically asks for 'gross written premium', 'GWP', or 'gross premium'",
                    "sql_example": "SELECT (COALESCE(T.DOC_PREMIUM, 0) + COALESCE(T.PRD_FEES4L, 0) - COALESCE(T.PRD_NPREM7L, 0) - COALESCE(T.PRD_NPREM8L, 0)) AS GROSS_WRITTEN_PREMIUM FROM insmv.AIMS_ALL_DATA T"
                },
                "critical_distinction": "PREMIUM ≠ GROSS WRITTEN PREMIUM - These are different concepts. Default to DOC_PREMIUM for general premium queries.",
                "user_query_mapping": {
                    "premium": "Use DOC_PREMIUM field",
                    "policy premium": "Use DOC_PREMIUM field", 
                    "premium amount": "Use DOC_PREMIUM field",
                    "gross premium": "Use gross written premium calculation",
                    "gross written premium": "Use gross written premium calculation",
                    "GWP": "Use gross written premium calculation"
                }
            },
            "gross_written_premium_formula": {
                "formula": "DOC_PREMIUM + PRD_FEES4L - PRD_NPREM7L - PRD_NPREM8L",
                "components": {
                    "DOC_PREMIUM": "Base premium amount (the standard field for premium queries)",
                    "PRD_FEES4L": "Policy fees for period 4",
                    "PRD_NPREM7L": "Net premium for period 7", 
                    "PRD_NPREM8L": "Net premium for period 8"
                },
                "business_logic": "Gross Written Premium represents the total premium amount including fees and adjustments across premium periods - USE ONLY when specifically requested",
                "sql_template": """SELECT 
    (
        COALESCE(T.DOC_PREMIUM, 0) 
        + COALESCE(T.PRD_FEES4L, 0) 
        - COALESCE(T.PRD_NPREM7L, 0) 
        - COALESCE(T.PRD_NPREM8L, 0)
    ) AS GROSS_WRITTEN_PREMIUM
FROM 
    insmv.AIMS_ALL_DATA T""",
                "sql_usage_notes": "Base template - add WHERE clauses, GROUP BY, and additional SELECT fields based on user's specific requirements. Use COALESCE to handle NULL values in premium calculations. ONLY use when user specifically asks for gross written premium."
            },
            "renewal_identification": "REN_POL_TYPE and linked via REN_POL_NO and REN_POL_YEAR",
            "open_claims": "Claims are open if CLAIM_CLOSE_DT is null",
            "outstanding_logic": "CLAIM_OS_VAL are 0 for closed claims",
            "premium_relationship": "PRD_Npremtl (after discount) = DOC_PREMIUM",
            "transaction_keys": "REN at end indicates renewal transaction"
        },
        
        # ======= CRITICAL SEARCH KEY PATTERNS =======
        "search_keys": {
            "claim_search_key": "claim branch + claim office + maj type + min type + claim no + claim acc year",
            "policy_search_key": "branch + office + maj type + min type + policy number + policy year", 
            "customer_search_patterns": {
                "specific_customer_lookup": "For finding specific customer information use: CUST_ID_NO (individual ID), DOC_CUST_NAME (name), phone fields, or COMP_EID_NO (company ID)",
                "customer_counting_aggregation": "DOC_CUST_SD_COD1 is used for counting customers in aggregate queries (e.g., 'count of customers in 2022')",
                "usage_distinction": "Use specific identifiers for individual customer details, use DOC_CUST_SD_COD1 for customer counts and statistics"
            },
            "claim_key_fields": "CLAIM_BRANCH + CLAIM_OFFICE + DOC_MAJ_INS_TYPE + DOC_MIN_INS_TYPE + CLAIM_NO + CLAIM_ACC_YEAR",
            "policy_key_fields": "DOC_BRANCH + DOC_OFFICE + DOC_MAJ_INS_TYPE + DOC_MIN_INS_TYPE + POL_NO + POL_YEAR",
            "search_best_practices": {
                "claim_lookup": "Use full claim key for precise claim identification",
                "policy_lookup": "Use full policy key for precise policy identification", 
                "specific_customer_lookup": "Use CUST_ID_NO, DOC_CUST_NAME, phone, or COMP_EID_NO for specific customer information",
                "customer_aggregation": "Use DOC_CUST_SD_COD1 for customer counting and statistical queries",
                "key_importance": "Always use complete keys for accurate searches - partial keys may return multiple matches"
            }
        },
        
        # ======= FIELD NAMING CONVENTIONS =======
        "field_patterns": {
            "code_vs_name_pattern": "Fields ending with _TYPE contain codes (1, 2, 3), fields ending with _NAME contain descriptive text",
            "code_fields": {
                "DOC_MAJ_INS_TYPE": "Major insurance type code (e.g., 29 = Motor) - Also called: line of business code, class code, insurance line code",
                "DOC_MIN_INS_TYPE": "Minor insurance type code (e.g., 111 = Comprehensive) - Also called: product code, subclass code, product type code",
                "DOC_BUS_TYPE": "Business type code (e.g., 1 = Direct)",
                "CLAIM_ACC_TYPE": "Accident type code (e.g., 4 = Material damage to third party)",
                "DOC_PLATE_TYPE": "Plate type code (e.g., 6 = Private - Trans.)",
                "PAY_SLIP_TYPE": "Payment slip type code"
            },
            "name_fields": {
                "DOC_MAJ_NAME": "Major insurance type name (e.g., Motor, Medical, Fire) - Also called: line of business, class, insurance line",
                "DOC_MIN_NAME": "Minor insurance type name (e.g., Comprehensive, Third Party) - Also called: product, subclass, product type",
                "DOC_BUS_NAME": "Business type name (e.g., Direct, Reinsurance, Co-Insurance)",
                "CLAIM_ACC_TYPE_NAME": "Accident type description (e.g., Material damage to third party vehicle)",
                "DOC_PLATE_TYPE_NAME": "Plate type name (e.g., Private, Taxi, Motor Cycle)",
                "PAY_SLIP_TYPE_NAME": "Payment slip type name (e.g., PAID, RECOVERY)"
            },
            "usage_guidelines": {
                "for_filtering": "Use _TYPE fields when filtering by specific codes, use _NAME fields when filtering by descriptive text",
                "for_display": "Use _NAME fields for user-friendly display, _TYPE fields for precise matching",
                "for_joins": "Both _TYPE and _NAME fields can be used, but _TYPE fields are typically more efficient",
                "user_queries": "When user asks for 'Motor insurance', use DOC_MAJ_NAME = 'Motor' OR DOC_MAJ_INS_TYPE = 29"
            },
            "alternative_terminology": {
                "major_field_aliases": "DOC_MAJ_INS_TYPE and DOC_MAJ_NAME can also be called: 'line of business', 'class', 'major type', or 'insurance line'",
                "minor_field_aliases": "DOC_MIN_INS_TYPE and DOC_MIN_NAME can also be called: 'product', 'subclass', 'minor type', or 'product type'",
                "user_query_mapping": {
                    "line of business": "Use DOC_MAJ_INS_TYPE or DOC_MAJ_NAME",
                    "class": "Use DOC_MAJ_INS_TYPE or DOC_MAJ_NAME", 
                    "product": "Use DOC_MIN_INS_TYPE or DOC_MIN_NAME",
                    "subclass": "Use DOC_MIN_INS_TYPE or DOC_MIN_NAME",
                    "insurance line": "Use DOC_MAJ_INS_TYPE or DOC_MAJ_NAME",
                    "product type": "Use DOC_MIN_INS_TYPE or DOC_MIN_NAME"
                },
                "important_note": "When users ask for 'product', 'subclass', 'line of business', or 'class', understand they are referring to the major/minor insurance type fields"
            }
        },
        
        # ======= POLICY INFORMATION =======
        "policy_identification": {
            "DOC_SERIAL": "Unique document serial number for each record",
            "DOC_PRIMARY_KEY": "Primary key identifier for the document",
            "DOC_KEY_FORM": "Transaction key (unique). REN at end means Renewal"
        },
        
        "branch_office": {
            "DOC_BRANCH": "Branch code (e.g. 1 = Main Branch)",
            "DOC_BRANCH_NAME": "Branch name description",
            "DOC_OFFICE": "Office code (e.g. 1 = Head Office)",
            "DOC_OFFICE_NAME": "Office name description",
            "DOC_ISSUE_OFFICE": "Issuing office code",
            "DOC_ISSUE_OFFICE_NAME": "Issuing office name"
        },
        
        "business_classification": {
            "DOC_BUS_TYPE": "Business type code (1 = Direct)",
            "DOC_BUS_NAME": "Business type description (Direct, etc.)",
            "DOC_MAJ_INS_TYPE": "Major insurance type code (29 = Motor)",
            "DOC_MAJ_NAME": "Major insurance type name (Motor) - Class of Insurance, Business ",
            "DOC_MIN_INS_TYPE": "Minor insurance type/subclass code (111 = Comp)",
            "DOC_MIN_NAME": "Minor insurance type name (Comp = Comprehensive)"
        },
        
        "critical_dates": {
            "DOC_REG_DT": "The date when the policy was registered on the system",
            "DOC_REG_TIME": "Time when policy was registered (in time format)",
            "DOC_ST_DT": "The date when the policy activated",
            "DOC_INS_ED_DT": "The policy is active until this date",
            "CLAIM_REG_DT": "Registration date (open if not null)",
            "CLAIM_ACC_DT": "Accident date",
            "CLAIM_NOTIF_DT": "Notification date (usually same as REG_DT)",
            "CLAIM_CLOSE_DT": "If null → claim is open"
        },
        
        "date_query_rules": {
            "year_based_queries": "When user asks for policies 'in [year]' (e.g., 'policies in 2022'), use DOC_REG_DT, not POL_YEAR",
            "registration_vs_policy_year": "DOC_REG_DT shows when policy was entered in system, POL_YEAR is policy document year",
            "user_intent_mapping": {
                "find policies in 2022": "Use WHERE EXTRACT(YEAR FROM DOC_REG_DT) = 2022",
                "policies from last year": "Use DOC_REG_DT for time-based filtering",
                "recent policies": "Use DOC_REG_DT for chronological queries",
                "policies registered this year": "Use DOC_REG_DT explicitly"
            },
            "pol_year_usage": "Use POL_YEAR only when specifically asking about policy document year, not general time queries"
        },
        
        "document_types": {
            "1": "Policy → DOC_NO = POL_NO | DOC_UW_YEAR = POL_YEAR",
            "2": "Additional/Policy → Additional for the policy (Endorsement)",
            "3": "Additional/Certificate → Additional for the certificate (Endorsement)",
            "4": "Renewal → DOC_NO = REN_POL_NO ≠ POL_NO | DOC_UW_YEAR = REN_POL_YEAR ≠ POL_YEAR. REN_POL_TYPE is 1 (new policy) or 4 (renewal policy)",
            "5": "Marine Certificate → DOC_NO = CER_NO | DOC_UW_YEAR = CER_YEAR. CER_NO and CER_YEAR are null if not certificate",
            "6": "Refund/Policy",
            "7": "Refund/Certificate"
        },
        
        "customer_information": {
            "individual_customer": "CUST_ID_NO not null, COMP_EID_NO null",
            "company_customer": "CUST_ID_NO null, COMP_EID_NO not null",
            "customer_fields": {
                "DOC_CUST_NAME": "Customer name (company or individual) - use for finding specific customer by name",
                "CUST_NATIONALITY": "Customer nationality code (2 = Qatar)",
                "CUST_ID_NO": "Individual customer ID - use for finding specific individual customer (null for companies)",
                "COMP_EID_NO": "Company ID - use for finding specific company customer (null for individuals)",
                "ACCOUNT_STATUS": "1 means valid account, 2 means invalid account",
                "phone_fields": "Phone number fields - use for finding specific customer by phone number"
            },
            "customer_search_usage": {
                "for_specific_customer": "Use CUST_ID_NO (individuals), COMP_EID_NO (companies), DOC_CUST_NAME (name), or phone fields",
                "for_customer_counting": "Use DOC_CUST_SD_COD1 for aggregate queries like 'count customers in 2022'",
                "examples": {
                    "find_customer_details": "WHERE CUST_ID_NO = '12345678901' OR DOC_CUST_NAME LIKE '%Customer Name%'",
                    "count_customers": "COUNT(DISTINCT DOC_CUST_SD_COD1) for customer statistics"
                }
            },
            "doc_cust_sd_cod1_usage": "Used specifically for customer counting and statistical aggregation, NOT for finding individual customer details"
        },
        
        "data_sources": {
            "DOC_SOURCE_NAME": "12 sources: Broker, Direct Business, Mobile app, Web, Call Center, etc.",
            "DOC_AGENT_NAME": "Agent/Broker name - NULL means DIRECT business (company sales), NOT NULL means BROKER business",
            "DOC_USER_NO": "Employees or Brokers who entered the policy",
            "DOC_USER_NAME": "Employee/Broker name who entered policy"
        },
        
        # ======= VEHICLE INFORMATION =======
        "vehicle_basic": {
            "DOC_PLATE_NO": "Vehicle plate number (e.g. 53023)",
            "DOC_CARD_NO": "Vehicle registration card number",
            "DOC_PLATE_COLOR": "Plate color code (1 = White) - 5 Plate Colors",
            "DOC_COLOR_NAME": "Plate color name (Red, Blue, Black, Green, White)"
        },
        
        "vehicle_specifications": {
            "DOC_MAKE": "Vehicle manufacturer code (1 = Nissan) - 628 Makes",
            "DOC_MAKE_NAME": "Vehicle manufacturer name (Nissan, Toyota, etc.)",
            "DOC_MODEL": "Vehicle model (URVAN, Skyline, Supra, etc.) - 6962 Models",
            "DOC_PROD_YEAR": "Vehicle production year",
            "DOC_BODY_TYPE": "Body type code (3 = Bus) - 251 Body Types",
            "DOC_BODY_NAME": "Body type description (Sport, Bus, Van, etc.)",
            "DOC_PLATE_TYPE": "Plate type code (6 = Private - Trans.) - 19 Plate Types",
            "DOC_PLATE_TYPE_NAME": "Plate type name (Private, Taxi, Motor Cycle, Private - Trans., etc.)"
        },
        
        "vehicle_technical": {
            "DOC_CYLENDER": "Engine cylinder count code (4 = 4 Cylinders) - 15 Cylinder Types",
            "DOC_CYLENDER_NAME": "Engine cylinder Name (4 Cylinders, 8 Cylinders, More than 8 Cylinders)",
            "DOC_LOAD": "Load capacity code",
            "DOC_LOAD_NAME": "Load capacity description (Like 10 tons, 5 tons, etc.)",
            "DOC_WEIGHT": "Vehicle weight code",
            "DOC_WEIGHT_NAME": "Vehicle weight description",
            "DOC_ENG_NO": "Engine number",
            "DOC_CHAS_NO": "Chassis number",
            "DOC_ENG_SIZE": "Engine size specification"
        },
        
        "driver_information": {
            "DOC_DRIVER_BDT": "Driver birth date",
            "DOC_DRIVER_AGE": "Driver age"
        },
        
        # ======= FINANCIAL INFORMATION =======
        "premium_coverage": {
            "DOC_SUM_INSURED": "Coverage amount provided by company",
            "DOC_PREMIUM": "Payment by user for coverage",
            "DOC_COMM": "Commission amount",
            "DOC_GOLD": "Gold sharing amount",
            "DOC_SILVER": "Silver sharing amount",
            "DOC_GULF": "Gulf sharing amount",
            "DOC_OURSHAR": "Our share amount"
        },
        
        "premium_breakdown_periods": {
            "net_premium": "PRD_NPREM1L to PRD_NPREM8L (8 periods), Total: PRD_NPREMTL",
            "premium": "PRD_PREM1L to PRD_PREM8L (8 periods), Total: PRD_PREMTL (Premium before discount)",
            "fees": "PRD_FEES1L to PRD_FEES6L (Policy fees)",
            "discount": "PRD_DISC1L to PRD_DISC8L (Discount amounts)",
            "total_discount": "PRD_TDISC1L to PRD_TDISC6L (Total discount per period)",
            "profit_commission": "PRD_PROFIT_COMM"
        },
        
        "coverage_details": {
            "COLOR": "Vehicle color",
            "SEATS": "Number of seats",
            "PASSENGERS_COVERS": "Passenger coverage indicator",
            "DRIVER_COVER": "Driver coverage indicator",
            "DEPRECIATION": "Depreciation information",
            "LIAB_LIMIT": "Liability limit",
            "EXCESS_PCNT": "Excess percentage",
            "EXCESS_AMOUNT": "Excess amount"
        },
        
        # ======= CLAIMS INFORMATION =======
        "claim_identification": {
            "CLAIM_BRANCH": "Claim branch code - 5 Branches",
            "CLAIM_OFFICE": "Claim office code - 31 offices",
            "CLAIM_NO": "Claim number",
            "CLAIM_ACC_YEAR": "Claim accident year"
        },
        
        "claim_details": {
            "CLAIM_ACC_TYPE": "Accident type code - 51 Different types, majority is 4 = Material damage to third party vehicle",
            "CLAIM_ACC_TYPE_NAME": "Accident type description",
            "CLAIM_CAUSE_OF_LOSS": "Cause of loss code",
            "CLAIM_CAUSE_NAME": "Cause of loss description",
            "CLAIM_ACC_PLACE": "Accident place code",
            "CLAIM_ACC_PLACE_NAME": "Accident place name",
            "CLAIM_STATUS": "Open or Close",
            "CLM_ACC_DESC": "Description of claim"
        },
        
        "claim_financials": {
            "CLAIM_OS_VAL": "Outstanding value (0 if closed)",
            "OS_RET": "Outstanding retention amount",
            "OS_QS": "Outstanding quota share amount",
            "OS_SP": "Outstanding surplus amount",
            "OS_FAC": "Outstanding facultative amount",
            "CLAIM_OS_REC_VAL": "Recovery value"
        },
        
        # ======= PAYMENTS INFORMATION =======
        "payment_identification": {
            "PAY_SLIP_NO": "Payment slip number",
            "PAY_SLIP_YEAR": "Payment slip year",
            "PAY_SLIP_TYPE": "Payment slip type code",
            "PAY_SLIP_TYPE_NAME": "PAID (to customer) / RECOVERY (from customer)"
        },
        
        "payment_details": {
            "PAY_TP_SERIAL": "Third party serial number",
            "PAY_TP_LNAME": "Owner or third-party",
            "PAY_SLIP_DT": "Payment date",
            "PAY_PAYMENT_TERM": "Payment term code",
            "PAY_PAYMENT_TERM_NAME": "Payment term description",
            "PAY_PAYEE_PARTY": "Payee party code",
            "PAY_PAYEE_PARTY_NAME": "Payee party name",
            "PAY_PAYEE": "Payee information",
            "PAY_SLIP_VALUEL": "Payment slip value",
            "PAY_AMT": "Payment amount (updates outstanding)",
            "PAY_REC_AMT": "Recovered amount"
        },
        
        "payment_reinsurance": {
            "PAY_RI_SLIP_SERIAL": "Reinsurance slip serial",
            "PAY_RI_SLIP_YEAR": "Reinsurance slip year",
            "PAY_RET": "Payment retention",
            "PAY_QS": "Payment quota share",
            "PAY_SP": "Payment surplus",
            "PAY_FAC": "Payment facultative",
            "PAY_COINS": "Payment coinsurance",
            "PAY_SRET": "Payment surplus retention"
        },
        
        # ======= REINSURANCE INFORMATION =======
        "reinsurance_types": {
            "facultative": "FAC_SUM_INS, FAC_PREM - Individual risk reinsurance",
            "coinsurance": "COINS_SUM_INS, COINS_PREM - Shared risk coverage",
            "retrocession": "RETROC_SUM_INS, RETROC_PREM - Reinsurer's reinsurance",
            "retention": "RET_SUM_INS, RET_PREM - Company retained portion",
            "quota_share": "QS_SUM_INS, QS_PREM - Proportional reinsurance",
            "surplus": "SP_SUM_INS, SP_PREM - Non-proportional reinsurance",
            "surplus_retention": "SRET_SUM_INS, SRET_PREM - Retained surplus portion",
            "fronting": "FRONTING_SUM_INS, FRONTING_PREM - Fronting arrangement"
        },
        
        "facultative_layers": {
            "layer_1": "FAC_PCNT1, FAC_PREM1, FAC_ACC1, FAC_ACC_NAME1",
            "layer_2": "FAC_PCNT2, FAC_PREM2, FAC_ACC2, FAC_ACC_NAME2",
            "layer_3": "FAC_PCNT3, FAC_PREM3, FAC_ACC3, FAC_ACC_NAME3",
            "layer_4": "FAC_PCNT4, FAC_PREM4, FAC_ACC4, FAC_ACC_NAME4",
            "layer_5": "FAC_PCNT5, FAC_PREM5, FAC_ACC5, FAC_ACC_NAME5"
        },
        
        # ======= DATA QUALITY METRICS =======
        "data_statistics": {
            "total_fields": "200+ data fields",
            "vehicle_makes": "628 vehicle manufacturers",
            "vehicle_models": "6,962 vehicle models",
            "plate_colors": "5 colors (Red, Blue, Black, Green, White)",
            "body_types": "251 body types (Sport, Bus, Van, etc.)",
            "plate_types": "19 types (Private, Taxi, Motor Cycle, etc.)",
            "cylinder_types": "15 cylinder types (4, 8, More than 8 Cylinders)",
            "accident_types": "51 accident types (majority: Material damage to third party)",
            "data_sources": "12 sources (Broker, Direct, Mobile, Web, etc.)",
            "claim_branches": "5 claims processing branches",
            "claim_offices": "31 claims processing offices"
        },
        
        # ======= RELATIONSHIPS AND JOINS =======
        "data_relationships": {
            "policy_to_claims": "Linked via policy identification fields",
            "claims_to_payments": "One claim can have multiple payments",
            "reinsurance_layers": "Up to 5 facultative layers per policy",
            "premium_periods": "Financial data split across 8 time periods",
            "voucher_system": "Separate vouchers for accounts and agents"
        }
    }


def format_domain_knowledge_for_planning(domain_knowledge: dict, user_question: str) -> str:
    """Format comprehensive domain knowledge for strategic planning"""
    # Ensure user_question is always a string
    user_question = str(user_question) if not isinstance(user_question, str) else user_question
    question_lower = user_question.lower()
    relevant_knowledge = []
    
    # Always include business rules - they're fundamental
    relevant_knowledge.append("=== BUSINESS RULES ===")
    for key, value in domain_knowledge['business_rules'].items():
        relevant_knowledge.append(f"• {key}: {value}")
    
    # Always include critical search key patterns - essential for queries
    relevant_knowledge.append("\n=== CRITICAL SEARCH KEY PATTERNS ===")
    for key, value in domain_knowledge['search_keys'].items():
        if isinstance(value, dict):
            relevant_knowledge.append(f"• {key.upper().replace('_', ' ')}:")
            for subkey, subvalue in value.items():
                relevant_knowledge.append(f"  - {subkey}: {subvalue}")
        else:
            relevant_knowledge.append(f"• {key}: {value}")
    
    # Always include field naming patterns - critical for correct field usage
    relevant_knowledge.append("\n=== FIELD NAMING CONVENTIONS ===")
    relevant_knowledge.append(f"• {domain_knowledge['field_patterns']['code_vs_name_pattern']}")
    relevant_knowledge.append("• CODE FIELDS (_TYPE): Contain numeric codes (1, 2, 3)")
    for field, desc in domain_knowledge['field_patterns']['code_fields'].items():
        relevant_knowledge.append(f"  - {field}: {desc}")
    relevant_knowledge.append("• NAME FIELDS (_NAME): Contain descriptive text")
    for field, desc in domain_knowledge['field_patterns']['name_fields'].items():
        relevant_knowledge.append(f"  - {field}: {desc}")
    relevant_knowledge.append("• USAGE GUIDELINES:")
    for guideline, desc in domain_knowledge['field_patterns']['usage_guidelines'].items():
        relevant_knowledge.append(f"  - {guideline}: {desc}")
    
    # Add alternative terminology information
    relevant_knowledge.append("• ALTERNATIVE TERMINOLOGY (CRITICAL FOR USER QUERIES):")
    relevant_knowledge.append(f"  - MAJOR FIELD ALIASES: {domain_knowledge['field_patterns']['alternative_terminology']['major_field_aliases']}")
    relevant_knowledge.append(f"  - MINOR FIELD ALIASES: {domain_knowledge['field_patterns']['alternative_terminology']['minor_field_aliases']}")
    relevant_knowledge.append("  - USER QUERY MAPPING:")
    for term, field in domain_knowledge['field_patterns']['alternative_terminology']['user_query_mapping'].items():
        relevant_knowledge.append(f"    * '{term}' → {field}")
    relevant_knowledge.append(f"  - {domain_knowledge['field_patterns']['alternative_terminology']['important_note']}")
    
    # Add organizational structure if relevant
    if any(word in question_lower for word in ['branch', 'office', 'organization', 'structure', 'takaful', 'shamel', 'main', 'international', 'india', 'lebanon', 'dubai', 'lulu', 'digital', 'channel', 'distribution']):
        relevant_knowledge.append("\n=== ORGANIZATIONAL STRUCTURE ===")
        for key, value in domain_knowledge['organizational_structure'].items():
            if isinstance(value, dict):
                relevant_knowledge.append(f"• {key}:")
                for subkey, subvalue in value.items():
                    relevant_knowledge.append(f"  - {subkey}: {subvalue}")
            elif isinstance(value, list):
                relevant_knowledge.append(f"• {key}: {', '.join(value[:10])}{'...' if len(value) > 10 else ''}")
            else:
                relevant_knowledge.append(f"• {key}: {value}")
    
    # Add lines of business if relevant
    if any(word in question_lower for word in ['motor', 'life', 'medical', 'fire', 'marine', 'aviation', 'energy', 'engineering', 'product', 'line', 'business', 'insurance']):
        relevant_knowledge.append("\n=== LINES OF BUSINESS ===")
        for key, value in domain_knowledge['lines_of_business'].items():
            relevant_knowledge.append(f"• {key}:")
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        relevant_knowledge.append(f"  - {subkey}: {', '.join(subvalue)}")
                    else:
                        relevant_knowledge.append(f"  - {subkey}: {subvalue}")
    
    # Add customer information if relevant
    if any(word in question_lower for word in ['customer', 'individual', 'company', 'corporate', 'client', 'cust']):
        relevant_knowledge.append("\n=== CUSTOMER INFORMATION ===")
        relevant_knowledge.append(f"• Individual: {domain_knowledge['customer_information']['individual_customer']}")
        relevant_knowledge.append(f"• Company: {domain_knowledge['customer_information']['company_customer']}")
        for key, value in domain_knowledge['customer_information']['customer_fields'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        
        relevant_knowledge.append("\n=== CUSTOMER SEARCH PATTERNS ===")
        for key, value in domain_knowledge['customer_information']['customer_search_usage'].items():
            if isinstance(value, dict):
                relevant_knowledge.append(f"• {key}:")
                for subkey, subvalue in value.items():
                    relevant_knowledge.append(f"  - {subkey}: {subvalue}")
            else:
                relevant_knowledge.append(f"• {key}: {value}")
        relevant_knowledge.append(f"• DOC_CUST_SD_COD1 Usage: {domain_knowledge['customer_information']['doc_cust_sd_cod1_usage']}")
    
    # Add vehicle information if relevant
    if any(word in question_lower for word in ['vehicle', 'car', 'plate', 'make', 'model', 'motor', 'engine', 'driver']):
        relevant_knowledge.append("\n=== VEHICLE INFORMATION ===")
        for key, value in domain_knowledge['vehicle_basic'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        for key, value in domain_knowledge['vehicle_specifications'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        relevant_knowledge.append("\n=== VEHICLE TECHNICAL ===")
        for key, value in domain_knowledge['vehicle_technical'].items():
            relevant_knowledge.append(f"• {key}: {value}")
    
    # Add financial information if relevant
    if any(word in question_lower for word in ['premium', 'price', 'cost', 'amount', 'financial', 'money', 'fee', 'coverage', 'sum', 'commission', 'loss', 'ratio', 'gross', 'written']):
        relevant_knowledge.append("\n=== FINANCIAL INFORMATION ===")
        for key, value in domain_knowledge['premium_coverage'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        relevant_knowledge.append("\n=== PREMIUM BREAKDOWN ===")
        for key, value in domain_knowledge['premium_breakdown_periods'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        
        # Add premium terminology distinctions for financial queries
        if 'premium_terminology_distinctions' in domain_knowledge['business_rules']:
            premium_terms = domain_knowledge['business_rules']['premium_terminology_distinctions']
            relevant_knowledge.append("\n=== CRITICAL PREMIUM TERMINOLOGY DISTINCTIONS ===")
            relevant_knowledge.append(f"• {premium_terms['critical_distinction']}")
            relevant_knowledge.append("\n• BASIC PREMIUM (DOC_PREMIUM):")
            relevant_knowledge.append(f"  - Field: {premium_terms['basic_premium']['field']}")
            relevant_knowledge.append(f"  - Description: {premium_terms['basic_premium']['description']}")
            relevant_knowledge.append(f"  - When to use: {premium_terms['basic_premium']['when_to_use']}")
            relevant_knowledge.append("\n• GROSS WRITTEN PREMIUM (CALCULATED):")
            relevant_knowledge.append(f"  - Formula: {premium_terms['gross_written_premium']['formula']}")
            relevant_knowledge.append(f"  - Description: {premium_terms['gross_written_premium']['description']}")
            relevant_knowledge.append(f"  - When to use: {premium_terms['gross_written_premium']['when_to_use']}")
            relevant_knowledge.append("\n• USER QUERY MAPPING:")
            for query_type, field_to_use in premium_terms['user_query_mapping'].items():
                relevant_knowledge.append(f"  - '{query_type}' → {field_to_use}")
        
        # Add loss ratio calculation details for financial queries
        if 'loss_ratio_formula' in domain_knowledge['business_rules']:
            loss_ratio = domain_knowledge['business_rules']['loss_ratio_formula']
            relevant_knowledge.append("\n=== LOSS RATIO CALCULATION ===")
            relevant_knowledge.append(f"• Formula: {loss_ratio['formula']}")
            relevant_knowledge.append(f"• Total PAY_AMT: {loss_ratio['total_pay_amt_calculation']}")
            relevant_knowledge.append("• Components:")
            for comp, desc in loss_ratio['components'].items():
                relevant_knowledge.append(f"  - {comp}: {desc}")
            relevant_knowledge.append(f"• Business Logic: {loss_ratio['business_logic']}")
            relevant_knowledge.append("\n• SQL TEMPLATE FOR LOSS RATIO:")
            relevant_knowledge.append(loss_ratio['sql_template'])
            relevant_knowledge.append(f"• Usage: {loss_ratio['sql_usage_notes']}")
        
        # Add gross written premium calculation details ONLY when specifically requested
        if any(word in question_lower for word in ['gross', 'written', 'gwp']) and 'gross_written_premium_formula' in domain_knowledge['business_rules']:
            gwp = domain_knowledge['business_rules']['gross_written_premium_formula']
            relevant_knowledge.append("\n=== GROSS WRITTEN PREMIUM CALCULATION ===")
            relevant_knowledge.append(f"• Formula: {gwp['formula']}")
            relevant_knowledge.append("• Components:")
            for comp, desc in gwp['components'].items():
                relevant_knowledge.append(f"  - {comp}: {desc}")
            relevant_knowledge.append(f"• Business Logic: {gwp['business_logic']}")
            relevant_knowledge.append("\n• SQL TEMPLATE FOR GROSS WRITTEN PREMIUM:")
            relevant_knowledge.append(gwp['sql_template'])
            relevant_knowledge.append(f"• Usage: {gwp['sql_usage_notes']}")
    
    # Add claims information if relevant
    if any(word in question_lower for word in ['claim', 'accident', 'damage', 'outstanding', 'loss']):
        relevant_knowledge.append("\n=== CLAIMS INFORMATION ===")
        for key, value in domain_knowledge['claim_identification'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        relevant_knowledge.append("\n=== CLAIM DETAILS ===")
        for key, value in domain_knowledge['claim_details'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        relevant_knowledge.append("\n=== CLAIM FINANCIALS ===")
        for key, value in domain_knowledge['claim_financials'].items():
            relevant_knowledge.append(f"• {key}: {value}")
    
    # Add payments information if relevant
    if any(word in question_lower for word in ['payment', 'pay', 'slip', 'recovery', 'paid']):
        relevant_knowledge.append("\n=== PAYMENTS INFORMATION ===")
        for key, value in domain_knowledge['payment_identification'].items():
            relevant_knowledge.append(f"• {key}: {value}")
        for key, value in domain_knowledge['payment_details'].items():
            relevant_knowledge.append(f"• {key}: {value}")
    
    # Add data sources if relevant
    if any(word in question_lower for word in ['source', 'agent', 'broker', 'direct', 'mobile', 'web']):
        relevant_knowledge.append("\n=== DATA SOURCES ===")
        for key, value in domain_knowledge['data_sources'].items():
            relevant_knowledge.append(f"• {key}: {value}")
    
    # Always include data statistics for context
    relevant_knowledge.append("\n=== DATA STATISTICS ===")
    for key, value in domain_knowledge['data_statistics'].items():
        relevant_knowledge.append(f"• {key}: {value}")
    
    # Always include relationships
    relevant_knowledge.append("\n=== DATA RELATIONSHIPS ===")
    for key, value in domain_knowledge['data_relationships'].items():
        relevant_knowledge.append(f"• {key}: {value}")
    
    # ALWAYS include policy counting rules (critical for accurate policy counts)
    relevant_knowledge.append("\n=== CRITICAL POLICY & TRANSACTION COUNTING RULES ===")
    policy_counting = domain_knowledge['business_rules']['policy_counting']
    relevant_knowledge.append(f"• **COUNTING FIELD**: {policy_counting['field_to_count']}")
    relevant_knowledge.append(f"• **DUAL COUNTING RULE**: {policy_counting['rule']}")
    relevant_knowledge.append(f"• **POLICY COUNT**: {policy_counting['policy_count']['description']} - {policy_counting['policy_count']['filter']}")
    relevant_knowledge.append(f"• **TRANSACTION COUNT**: {policy_counting['transaction_count']['description']} - {policy_counting['transaction_count']['filter']}")
    relevant_knowledge.append(f"• **DUAL COUNT QUERY TEMPLATE**: {policy_counting['dual_count_query_template']}")
    relevant_knowledge.append(f"• **BASIC COUNT EXAMPLE**: {policy_counting['example_queries']['basic_count']}")
    relevant_knowledge.append(f"• **DOC_TYPE MEANINGS**: 1={policy_counting['doc_type_meanings']['1']}, 4={policy_counting['doc_type_meanings']['4']}, Others={policy_counting['doc_type_meanings']['others']}")
    relevant_knowledge.append(f"• **RESPONSE FORMAT**: {policy_counting['response_format']}")
    relevant_knowledge.append(f"• **CRITICAL REMINDER**: {policy_counting['critical_reminder']}")
    relevant_knowledge.append(f"• **IMPORTANT NOTE**: {policy_counting['important_note']}")
    
    # ALWAYS include customer identification rules (critical for accurate customer searches)
    relevant_knowledge.append("\n=== CRITICAL CUSTOMER IDENTIFICATION RULES ===")
    customer_id = domain_knowledge['business_rules']['customer_identification']
    relevant_knowledge.append(f"• **PRIMARY CUSTOMER ID**: {customer_id['primary_customer_id']} (National ID - most commonly used)")
    relevant_knowledge.append(f"• **CUSTOMER CODE**: {customer_id['customer_code']} (Internal system code)")
    relevant_knowledge.append(f"• **KEY DISTINCTION**: {customer_id['key_distinction']}")
    relevant_knowledge.append(f"• **USAGE PRIORITY**: {customer_id['usage_priority']}")
    relevant_knowledge.append(f"• **CUST_ID_NO**: {customer_id['field_meanings']['CUST_ID_NO']}")
    relevant_knowledge.append(f"• **DOC_CUST_SL_COD1**: {customer_id['field_meanings']['DOC_CUST_SL_COD1']}")
    relevant_knowledge.append(f"• **TERMINOLOGY NOTE**: {customer_id['terminology_note']}")
    relevant_knowledge.append(f"• **IMPORTANT NOTE**: {customer_id['important_note']}")
    
    # ALWAYS include complete results requirement (critical for comprehensive responses)
    relevant_knowledge.append("\n=== CRITICAL RESULT COMPLETENESS RULES ===")
    relevant_knowledge.append("• **COMPLETE RESULTS REQUIRED**: Always return ALL query results without truncation or limiting")
    relevant_knowledge.append("• **NO ARBITRARY LIMITS**: Do NOT add ROWNUM limits unless user explicitly requests specific count")
    relevant_knowledge.append("• **FULL DATA ANALYSIS**: Process and analyze complete result sets, not just samples or previews")
    relevant_knowledge.append("• **USER EXPECTATION**: Users expect comprehensive responses with all relevant data included")
    relevant_knowledge.append("• **ONLY LIMIT WHEN REQUESTED**: Add ROWNUM only for explicit requests like 'top 5', 'first 10', 'limit 20'")
    
    # ALWAYS include agent/broker business rules (critical for business analysis)
    relevant_knowledge.append("\n=== CRITICAL AGENT/BROKER BUSINESS RULES ===")
    agent_broker = domain_knowledge['business_rules']['agent_broker_business']
    relevant_knowledge.append(f"• **DIRECT BUSINESS**: {agent_broker['direct_business_rule']}")
    relevant_knowledge.append(f"• **BROKER BUSINESS**: {agent_broker['broker_business_rule']}")
    relevant_knowledge.append(f"• **DIRECT CLASSIFICATION**: {agent_broker['business_classification']['direct']}")
    relevant_knowledge.append(f"• **BROKER CLASSIFICATION**: {agent_broker['business_classification']['broker']}")
    relevant_knowledge.append(f"• **IMPORTANCE**: {agent_broker['important_note']}")
    
    return '\n'.join(relevant_knowledge)
