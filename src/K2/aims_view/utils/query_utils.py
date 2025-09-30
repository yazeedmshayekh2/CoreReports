"""
Query utilities for SQL cleaning and validation
"""


def clean_query(sql_query: str) -> str:
    """Clean and validate SQL query"""
    # Remove markdown formatting
    if "```sql" in sql_query:
        sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
    elif "```" in sql_query:
        sql_query = sql_query.split("```")[1].split("```")[0].strip()
    
    # Remove extra whitespace
    sql_query = " ".join(sql_query.split())
    
    # Remove trailing semicolon if present
    sql_query = sql_query.rstrip(';').strip()
    
    return sql_query


def build_execution_context(execution_history: list, accumulated_results: dict, cycle: int) -> str:
    """Build context from previous execution cycles"""
    if cycle == 1:
        return "First cycle - no previous context"
    
    context = f"Previous cycles: {cycle-1}\n"
    if execution_history:
        context += f"Previous queries executed: {len(execution_history)}\n"
    if accumulated_results:
        context += f"Accumulated results: {list(accumulated_results.keys())}\n"
    return context


def format_results_summary(execution_result: dict) -> str:
    """Format execution results for response generation"""
    results_summary = "QUERY RESULTS SUMMARY:\n"
    for key, result in execution_result.get('results', {}).items():
        if 'results' in result:
            row_count = result.get('row_count', 0)
            results_summary += f"\n{key.upper()} ({row_count} rows):\n"
            
            if isinstance(result['results'], list) and len(result['results']) > 0:
                # Show ALL results for complete analysis (no truncation)
                for i, row in enumerate(result['results']):
                    results_summary += f"  Row {i+1}: {str(row)}\n"
                    
            if 'computation' in str(key).lower() and isinstance(result, dict):
                # Include computational results
                for comp_key in ['calculation_type', 'result', 'formula_used', 'business_interpretation']:
                    if comp_key in result:
                        results_summary += f"  {comp_key}: {result[comp_key]}\n"
    
    return results_summary


def format_data_sources_summary(intermediate_data: dict) -> str:
    """Format data sources for computational analysis"""
    data_summary = "AVAILABLE DATA SOURCES:\n"
    for step_key, step_data in intermediate_data.items():
        if 'results' in step_data and step_data['results']:
            data_summary += f"\n{step_key.upper()} ({step_data['row_count']} rows):\n"
            data_summary += f"  Description: {step_data.get('step_description', 'Query results')}\n"
            
            # Show sample data structure
            if isinstance(step_data['results'], list) and len(step_data['results']) > 0:
                sample_record = step_data['results'][0]
                if isinstance(sample_record, dict):
                    data_summary += f"  Columns: {list(sample_record.keys())}\n"
                    # Show sample values for numeric columns
                    numeric_samples = {k: v for k, v in sample_record.items() if isinstance(v, (int, float)) and v is not None}
                    if numeric_samples:
                        data_summary += f"  Sample numeric values: {numeric_samples}\n"
    
    return data_summary
