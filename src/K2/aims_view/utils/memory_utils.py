"""
Simple Memory Management Utilities for K2 AI Assistant
Handles conversation memory for context continuity
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class SimpleMemoryManager:
    """Simple memory management for conversation context"""
    
    def __init__(self, memory_file_path: str, memory_size: int = 5):
        self.memory_file = Path(memory_file_path)
        self.memory_size = memory_size
        
    def load_memory(self) -> dict:
        """Load conversation memory from JSON file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._create_empty_memory()
        except Exception as e:
            print(f"⚠️ Error loading memory: {str(e)}")
            return self._create_empty_memory()
    
    def _create_empty_memory(self) -> dict:
        """Create initial memory structure"""
        return {
            "memory_size": self.memory_size,
            "current_session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "conversations": [],
            "last_updated": datetime.now().isoformat()
        }
    
    def save_conversation(self, memory: dict, question: str, answer: str, metadata: dict = None):
        """Save Q&A pair to memory"""
        try:
            # Create memory directory if it doesn't exist
            self.memory_file.parent.mkdir(parents=True, exist_ok=True)
            
            conversation_entry = {
                "timestamp": datetime.now().isoformat(),
                "session_id": memory.get("current_session_id", f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
                "question": question,
                "answer": answer,
                "metadata": metadata or {}
            }
            
            # Add to conversations list
            memory["conversations"].append(conversation_entry)
            
            # Keep only last N conversations
            if len(memory["conversations"]) > self.memory_size:
                memory["conversations"] = memory["conversations"][-self.memory_size:]
            
            memory["last_updated"] = datetime.now().isoformat()
            
            # Save to file
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Error saving memory: {str(e)}")
    
    @staticmethod
    def get_memory_context(memory: dict, current_question: str) -> str:
        """Extract relevant context from memory for current question"""
        if not memory.get("conversations"):
            return ""
        
        context_parts = []
        
        # Check if current question relates to previous conversations
        for conv in reversed(memory["conversations"][-3:]):  # Check last 3 conversations
            prev_question = conv.get("question", "")
            prev_answer = conv.get("answer", "")
            
            # Simple context detection
            if SimpleMemoryManager.is_related_question(current_question, prev_question):
                # Extract key information from previous conversation
                extracted_info = SimpleMemoryManager.extract_key_info(prev_question, prev_answer)
                if extracted_info:
                    context_parts.append(f"Previous context: {extracted_info}")
        
        if context_parts:
            return "MEMORY CONTEXT FROM RECENT CONVERSATIONS:\n" + "\n".join(context_parts) + "\n\n"
        
        return ""
    
    @staticmethod
    def is_related_question(current: str, previous: str) -> bool:
        """Check if current question relates to previous one using simple keyword matching"""
        # Extract potential customer IDs (11 digit numbers)
        current_ids = re.findall(r'\b\d{11}\b', current)
        previous_ids = re.findall(r'\b\d{11}\b', previous)
        
        # Check for common customer IDs
        if current_ids and previous_ids and any(id in previous_ids for id in current_ids):
            return True
        
        # Extract potential customer names
        current_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', current)
        previous_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', previous)
        
        # Check for common names
        if current_names and previous_names and any(name in previous_names for name in current_names):
            return True
        
        # Check for continuation keywords
        continuation_keywords = ['same', 'this', 'that', 'also', 'additionally', 'more', 'further', 'his', 'her']
        if any(keyword in current.lower() for keyword in continuation_keywords):
            return True
        
        return False
    
    @staticmethod
    def extract_key_info(question: str, answer: str) -> str:
        """Extract key information from previous Q&A"""
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

    @staticmethod
    def clear_memory(memory_file_path: str):
        """Clear all memory (useful for testing or reset)"""
        try:
            memory_file = Path(memory_file_path)
            if memory_file.exists():
                memory_file.unlink()
                print("✅ Memory cleared successfully")
        except Exception as e:
            print(f"⚠️ Error clearing memory: {str(e)}")
    
    @staticmethod
    def print_memory_summary(memory: dict):
        """Print a summary of current memory"""
        conversations = memory.get("conversations", [])
        print(f"💭 Memory Summary: {len(conversations)} conversations stored")
        for i, conv in enumerate(conversations[-3:], 1):  # Show last 3
            question = conv.get("question", "")[:50] + "..." if len(conv.get("question", "")) > 50 else conv.get("question", "")
            timestamp = conv.get("timestamp", "")[:19] if conv.get("timestamp") else ""
            print(f"  {i}. [{timestamp}] {question}")


# Example usage for testing
if __name__ == "__main__":
    # Test the memory manager
    memory_file = "/tmp/test_memory.json"
    manager = SimpleMemoryManager(memory_file, memory_size=3)
    
    # Load memory
    memory = manager.load_memory()
    
    # Save a conversation
    manager.save_conversation(
        memory, 
        "How many policies does customer 28140001175 have?",
        "Customer 28140001175 has 30 policies in total.",
        {"confidence": 0.95, "status": "success"}
    )
    
    # Test context retrieval
    context = SimpleMemoryManager.get_memory_context(memory, "What about his claims?")
    print("Context found:", context)
    
    # Print summary
    SimpleMemoryManager.print_memory_summary(memory)
