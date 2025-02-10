# base_agent.py
import os
from typing import Optional, Dict, Any
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.config_manager import ConfigManager

class BaseAgent:
    def __init__(self, temperature: float = 0.3, model_name: str = "mixtral-8x7b-32768"):
        # Initialize configuration manager
        self.config = ConfigManager()
        self.config.load_env_vars()
        
        # Configure Groq API
        self.groq_api_key = self.config.get("groq_api_key")
        if not self.groq_api_key:
            raise ValueError("❌ GROQ_API_KEY missing from configuration")
        
        # Initialize LLM
        self.llm = ChatGroq(
            temperature=temperature,
            model_name=model_name,
            groq_api_key=self.groq_api_key
        )
        
        # Initialize chain and prompt as None
        self.chain: Optional[LLMChain] = None
        self.prompt: Optional[PromptTemplate] = None
    
    def _initialize_chain(self, prompt_template: str, input_variables: list):
        """Initialize LangChain with prompt template"""
        self.prompt = PromptTemplate(
            input_variables=input_variables,
            template=prompt_template
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    def _handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Standardized error handling"""
        error_msg = f"⚠️ Error{f' in {context}' if context else ''}: {str(error)}"
        print(error_msg)
        return {
            'success': False,
            'error': error_msg,
            'data': None
        }
    
    def _format_response(self, data: Any, success: bool = True, error: str = None) -> Dict[str, Any]:
        """Standardized response format"""
        return {
            'success': success,
            'error': error,
            'data': data
        }
    
    def run(self, *args, **kwargs):
        """Abstract method to be implemented by child classes"""
        raise NotImplementedError("Subclasses must implement run()")