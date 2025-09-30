"""
LLM Factory for creating different AI model instances
"""

import os
from crewai import LLM


class LLMFactory:
    """Factory class for creating different LLM instances"""
    
    def __init__(self, config: dict):
        self.config = config
    
    def create_gemini_llm(self, stream: bool = False) -> LLM:
        """Create Gemini LLM instance for intelligent reasoning"""
        gemini_config = self.config["agents"]["router"]["models"]["gemini_model"]
        
        return LLM(
            model=gemini_config["model_name"],
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=gemini_config["temperature"],
            max_tokens=gemini_config["max_tokens"],
            stream=stream
        )
    
    def create_gemini_pro_llm(self, stream: bool = False) -> LLM:
        """Create Gemini Pro LLM instance for intelligent reasoning"""
        gemini_pro_config = self.config["agents"]["router"]["models"]["gemini_pro_model"]
        
        return LLM(
            model=gemini_pro_config["model_name"],
            api_key=os.getenv("GEMINI_API_KEY"),
            temperature=gemini_pro_config["temperature"],
            max_tokens=gemini_pro_config["max_tokens"],
            stream=stream
        )
    
    def create_gemini_streaming_llm(self) -> LLM:
        """Create Gemini LLM instance with streaming enabled for real-time response generation"""
        return self.create_gemini_llm(stream=True)
    
    def create_groq_llm(self, stream: bool = False) -> LLM:
        """Create Groq LLM instance"""
        groq_config = self.config["agents"]["router"]["models"]["groq_model"]
        
        return LLM(
            model=groq_config["model_name"],
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=groq_config["temperature"],
            max_tokens=groq_config["max_tokens"],
            stream=stream
        )
    
    def create_tools_groq_llm(self) -> LLM:
        """Create Groq LLM instance specifically for tools"""
        tools_config = self.config["agents"]["tools"]["models"]["groq_model"]
        
        return LLM(
            model=tools_config["model_name"],
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=tools_config["temperature"],
            max_tokens=tools_config["max_tokens"]
        )
    
    def get_ai_model_config(self) -> dict:
        """Get AI model configuration"""
        return self.config.get("ai", {})
    
    def validate_api_keys(self) -> dict:
        """Validate that required API keys are present"""
        validation_results = {
            "gemini_api_key": bool(os.getenv("GEMINI_API_KEY")),
            "groq_api_key": bool(os.getenv("GROQ_API_KEY"))
        }
        
        return validation_results
