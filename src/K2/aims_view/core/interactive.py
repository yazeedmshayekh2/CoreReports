"""
Interactive interfaces for the Intelligence Manager
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent.parent.parent)
sys.path.insert(0, project_root)

from src.K2.aims_view.agents.intelligence_manager import IntelligentSQLManager
import json


def interactive_intelligent_manager():
    """Interactive session with the Master Intelligence Manager"""
    print("🚀 MASTER INTELLIGENCE MANAGER ACTIVATED!")
    print("="*70)
    print("🧠 Autonomous SQL Problem Solving System")
    print("🎯 I will work persistently until your questions are fully answered")
    print("🔄 Self-optimizing • Self-managing • Self-evaluating")
    print("📚 Powered by AIMS Database Domain Knowledge + Google Gemini AI")
    print("="*70)
    
    # Check environment variables
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: Please set your GEMINI_API_KEY environment variable")
        return
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    
    manager = IntelligentSQLManager(config)
    
    print("\n🤖 Master Intelligence Manager Ready!")
    print("Ask me any complex question about insurance data - I'll solve it completely!")
    print("🔍 I have comprehensive knowledge of AIMS database structure and business rules.")
    print("Type 'quit', 'exit', or 'bye' to stop.\n")
    
    while True:
        try:
            user_input = input("🎯 Your question: ").strip()
            
            if str(user_input).lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("👋 Master Intelligence Manager shutting down. Thank you!")
                break
            
            if not user_input:
                print("Please enter your question about the insurance data.")
                continue
            
            print(f"\n{'='*70}")
            print(f"🔍 Processing: {user_input}")
            print('='*70)
            
            # The Master Intelligence Manager takes full control (reduced cycles for efficiency)
            result = manager.solve_intelligently(user_input, max_cycles=3)
            
            # Present results intelligently based on Master Intelligence Manager format
            if result.get('status') == 'success':
                print(f"\n🎉 COMPLETE SOLUTION ACHIEVED!")
                print(f"✅ Confidence: {result.get('confidence', 0.9)*100:.1f}%")
                print(f"🔄 Solved in {result.get('cycles_used', 0)} intelligence cycles")
                
                # Show the comprehensive response (already streamed during generation)
                response_text = result.get('response', '')
                if response_text:
                    print(f"\n📋 FINAL COMPREHENSIVE ANSWER:")
                    print("="*70)
                    print(response_text)
                    print("="*70)
                else:
                    print(f"📊 Summary: {result.get('summary', 'Solution provided')}")
                
                # Show technical details if needed (abbreviated)
                execution_summary = result.get('execution_summary', {})
                if execution_summary.get('executed_queries'):
                    print(f"\n🔍 Technical Details:")
                    print(f"  • Queries executed: {len(execution_summary.get('executed_queries', []))}")
                    if execution_summary.get('action') == 'QUERY_COMPUTE':
                        print(f"  • Computational analysis performed")
                    if execution_summary.get('intermediate_data'):
                        print(f"  • Data processing steps: {len(execution_summary.get('intermediate_data', {}))}")
                        
            elif result.get('status') == 'partial':
                print(f"\n📋 PARTIAL SOLUTION PROVIDED")
                print(f"⚠️  Used {result.get('cycles_used', 0)} cycles")
                print(f"📊 Results: {len(result.get('accumulated_results', {}))} components found")
                
            elif result.get('status') == 'error':
                print(f"\n❌ SYSTEM ERROR")
                print(f"💡 {result.get('message', 'Unknown error occurred')}")
            else:
                print(f"❌ Unexpected result format: {result}")
            
            print(f"\n🔄 Master Intelligence cycles used: {result.get('cycles_used', 0)}")
            print(f"\n{'='*70}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Master Intelligence Manager shutting down. Thank you!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("🔄 System recovering... Please try again.")


def demo_intelligent_manager():
    """Demonstration of the Master Intelligence Manager"""
    print("🎬 DEMO: Master Intelligence Manager")
    print("="*70)
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: Please set your GEMINI_API_KEY environment variable")
        return
    
    # Load configuration
    config_path = Path(__file__).parent.parent / "config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    
    manager = IntelligentSQLManager(config)
    
    # Demo questions showcasing intelligence
    demo_questions = [
        {
            "question": "Find me all high-value motor insurance policies from the main branch",
            "description": "Tests: multi-step planning, value interpretation, branch filtering"
        },
        {
            "question": "Which customers have claims that exceed their premium amounts?",
            "description": "Tests: complex relationships, cross-referencing, business logic"
        },
        {
            "question": "Show me insurance trends over time by policy type",
            "description": "Tests: temporal analysis, categorization, trend detection"
        }
    ]
    
    for i, demo in enumerate(demo_questions, 1):
        print(f"\n🎯 Demo {i}: {demo['question']}")
        print(f"🧪 Testing: {demo['description']}")
        print("-" * 70)
        
        try:
            result = manager.solve_intelligently(demo['question'], max_cycles=3)
            
            status = result.get('status', 'unknown')
            if status == 'success':
                print(f"✅ COMPLETE: {result.get('summary', 'Solved successfully')}")
            elif status == 'partial':
                print(f"📋 PARTIAL: Found {len(result.get('accumulated_results', {}))} components")
            else:
                print(f"❌ ISSUE: {result.get('message', 'Demo failed')}")
                
        except Exception as e:
            print(f"❌ Demo failed: {str(e)}")
        
        print("=" * 70)


def interactive_sql_agent():
    """🚀 Master Intelligence Manager - Interactive Session"""
    print("🚀 MASTER INTELLIGENCE MANAGER ACTIVATED!")
    print("="*70)
    print("🧠 Autonomous SQL Problem Solving System")
    print("🎯 I will work persistently until your questions are fully answered")
    print("🔄 Self-optimizing • Self-managing • Self-evaluating")
    print("📚 Powered by AIMS Database Domain Knowledge + Google Gemini AI")
    print("="*70)
    
    # Check environment variables
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: Please set your GEMINI_API_KEY environment variable")
        return
    
    manager = IntelligentSQLManager()
    
    print("\n🤖 Master Intelligence Manager Ready!")
    print("Ask me any complex question about insurance data - I'll solve it completely!")
    print("🔍 I have comprehensive knowledge of AIMS database structure and business rules.")
    print("Type 'quit', 'exit', or 'bye' to stop.\n")
    
    while True:
        try:
            user_input = input("🎯 Your question: ").strip()
            
            if str(user_input).lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("👋 Master Intelligence Manager shutting down. Thank you!")
                break
            
            if not user_input:
                print("Please enter your question about the insurance data.")
                continue
            
            print(f"\n{'='*70}")
            print(f"🔍 Processing: {user_input}")
            print('='*70)
            
            # The Master Intelligence Manager takes full control (reduced cycles for efficiency)
            result = manager.solve_intelligently(user_input, max_cycles=3)
            
            # Present results intelligently based on Master Intelligence Manager format
            if result.get('status') == 'success':
                print(f"\n🎉 COMPLETE SOLUTION ACHIEVED!")
                print(f"✅ Confidence: {result.get('confidence', 0.9)*100:.1f}%")
                print(f"🔄 Solved in {result.get('cycles_used', 0)} intelligence cycles")
                
                # Show the comprehensive response (already streamed during generation)
                response_text = result.get('response', '')
                if response_text:
                    print(f"\n📋 FINAL COMPREHENSIVE ANSWER:")
                    print("="*70)
                    print(response_text)
                    print("="*70)
                else:
                    print(f"📊 Summary: {result.get('summary', 'Solution provided')}")
                
                # Show technical details if needed (abbreviated)
                execution_summary = result.get('execution_summary', {})
                if execution_summary.get('executed_queries'):
                    print(f"\n🔍 Technical Details:")
                    print(f"  • Queries executed: {len(execution_summary.get('executed_queries', []))}")
                    if execution_summary.get('action') == 'QUERY_COMPUTE':
                        print(f"  • Computational analysis performed")
                    if execution_summary.get('intermediate_data'):
                        print(f"  • Data processing steps: {len(execution_summary.get('intermediate_data', {}))}")
                        
            elif result.get('status') == 'partial':
                print(f"\n📋 PARTIAL SOLUTION PROVIDED")
                print(f"⚠️  Used {result.get('cycles_used', 0)} cycles")
                print(f"📊 Results: {len(result.get('accumulated_results', {}))} components found")
                
            elif result.get('status') == 'error':
                print(f"\n❌ SYSTEM ERROR")
                print(f"💡 {result.get('message', 'Unknown error occurred')}")
            else:
                print(f"❌ Unexpected result format: {result}")
            
            print(f"\n🔄 Master Intelligence cycles used: {result.get('cycles_used', 0)}")
            print(f"\n{'='*70}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Master Intelligence Manager shutting down. Thank you!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("🔄 System recovering... Please try again.")
