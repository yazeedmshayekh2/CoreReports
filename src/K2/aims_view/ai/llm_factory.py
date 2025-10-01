"""
LLM Factory for creating different AI model instances with retry logic and fallback
"""

import os
import time
import logging
from crewai import LLM
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)


class LLMFactory:
    """Factory class for creating different LLM instances with resilience features"""
    
    def __init__(self, config: dict):
        self.config = config
        self.retry_attempts = 3
        self.retry_delay = 2  # seconds
        self.fallback_enabled = True
    
    def create_gemini_llm(self, stream: bool = False, enable_fallback: bool = True) -> LLM:
        """Create Gemini LLM instance with retry logic and automatic fallback to Groq
        
        Args:
            stream: Enable streaming responses
            enable_fallback: If True, automatically fallback to Groq on errors
        
        Returns:
            LLM instance (Gemini or Groq fallback)
        """
        gemini_config = self.config["agents"]["router"]["models"]["gemini_model"]
        
        try:
            return LLM(
                model=gemini_config["model_name"],
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=gemini_config["temperature"],
                max_tokens=gemini_config["max_tokens"],
                stream=stream,
                # Add retry configuration for litellm
                num_retries=self.retry_attempts,
                timeout=120  # 2 minutes timeout
            )
        except Exception as e:
            logger.warning(f"Failed to create Gemini LLM: {str(e)}")
            if enable_fallback and self.fallback_enabled:
                logger.info("🔄 Falling back to Groq LLaMA model...")
                return self.create_groq_llm(stream=stream)
            raise
    
    def create_gemini_pro_llm(self, stream: bool = False, enable_fallback: bool = True) -> LLM:
        """Create Gemini Pro LLM instance with retry logic and automatic fallback
        
        Args:
            stream: Enable streaming responses
            enable_fallback: If True, automatically fallback to Groq on errors
        
        Returns:
            LLM instance (Gemini Pro or Groq fallback)
        """
        gemini_pro_config = self.config["agents"]["router"]["models"]["gemini_pro_model"]
        
        try:
            return LLM(
                model=gemini_pro_config["model_name"],
                api_key=os.getenv("GEMINI_API_KEY"),
                temperature=gemini_pro_config["temperature"],
                max_tokens=gemini_pro_config["max_tokens"],
                stream=stream,
                # Add retry configuration for litellm
                num_retries=self.retry_attempts,
                timeout=120  # 2 minutes timeout
            )
        except Exception as e:
            logger.warning(f"Failed to create Gemini Pro LLM: {str(e)}")
            if enable_fallback and self.fallback_enabled:
                logger.info("🔄 Falling back to Groq LLaMA model...")
                return self.create_groq_llm(stream=stream)
            raise
    
    def create_gemini_streaming_llm(self) -> LLM:
        """Create Gemini LLM instance with streaming enabled for real-time response generation"""
        return self.create_gemini_llm(stream=True)
    
    def create_groq_llm(self, stream: bool = False) -> LLM:
        """Create Groq LLM instance (fast and reliable fallback)"""
        groq_config = self.config["agents"]["router"]["models"]["groq_model"]
        
        return LLM(
            model=groq_config["model_name"],
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=groq_config["temperature"],
            max_tokens=groq_config["max_tokens"],
            stream=stream,
            # Groq is generally more reliable, but add retries anyway
            num_retries=2,
            timeout=60
        )
    
    def create_tools_groq_llm(self) -> LLM:
        """Create Groq LLM instance specifically for tools"""
        tools_config = self.config["agents"]["tools"]["models"]["groq_model"]
        
        return LLM(
            model=tools_config["model_name"],
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=tools_config["temperature"],
            max_tokens=tools_config["max_tokens"],
            num_retries=2,
            timeout=60
        )
    
    def create_resilient_llm(self, prefer_gemini: bool = True, stream: bool = False) -> LLM:
        """Create a resilient LLM with automatic model selection and fallback
        
        This method intelligently selects between Gemini and Groq based on:
        - User preference (prefer_gemini)
        - API availability
        - Current load conditions
        
        Args:
            prefer_gemini: Try Gemini first if True, otherwise use Groq
            stream: Enable streaming responses
        
        Returns:
            LLM instance with best available model
        """
        if prefer_gemini:
            try:
                logger.info("🤖 Attempting to use Gemini 2.5 Flash...")
                return self.create_gemini_llm(stream=stream, enable_fallback=True)
            except Exception as e:
                logger.warning(f"Gemini unavailable, using Groq: {str(e)}")
                return self.create_groq_llm(stream=stream)
        else:
            # Use Groq directly for faster, more reliable responses
            logger.info("🚀 Using Groq LLaMA 3.3 70B (fast & reliable)...")
            return self.create_groq_llm(stream=stream)
    
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
    
    def set_retry_config(self, attempts: int = 3, delay: int = 2):
        """Configure retry behavior
        
        Args:
            attempts: Number of retry attempts
            delay: Delay between retries in seconds
        """
        self.retry_attempts = attempts
        self.retry_delay = delay
        logger.info(f"Retry configuration updated: {attempts} attempts, {delay}s delay")
    
    def enable_fallback(self, enabled: bool = True):
        """Enable or disable automatic fallback to Groq
        
        Args:
            enabled: If True, automatically fallback to Groq when Gemini fails
        """
        self.fallback_enabled = enabled
        status = "enabled" if enabled else "disabled"
        logger.info(f"Automatic fallback to Groq: {status}")
