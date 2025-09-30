"""
Main entry point for K2 Insurance AI Assistant Intelligence System
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.parent.parent.parent)
print(f"Adding project root to Python path: {project_root}")
sys.path.insert(0, project_root)

# Configure SSL before any AI imports
from src.K2.aims_view.security.ssl_config import configure_ssl_bypass
configure_ssl_bypass()

from src.K2.aims_view.core.interactive import interactive_intelligent_manager, demo_intelligent_manager


def main():
    """Main function to run the K2 Insurance AI Assistant Intelligence System"""
    print("Initializing K2 Insurance AI Assistant Intelligence System...")
    
    # Check for required environment variables
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: Please set your GEMINI_API_KEY environment variable")
        return
    
    if not os.getenv("GROQ_API_KEY"):
        print("Error: Please set your GROQ_API_KEY environment variable")
        return
    
    print("\n" + "="*70)
    print("K2 INSURANCE AI ASSISTANT - INTELLIGENCE SYSTEM")
    print("="*70)
    
    # Start interactive session
    interactive_intelligent_manager()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo_intelligent_manager()
        elif sys.argv[1] == "interactive":
            interactive_intelligent_manager()
        else:
            print("Usage: python main.py [demo|interactive]")
            print("  demo        - Run demonstration of Master Intelligence Manager")
            print("  interactive - Start interactive problem-solving session")
    else:
        # Default to main function
        main()
