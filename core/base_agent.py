# base_agent.py
import os
from typing import Optional, Dict, Any
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from utils.config_manager import ConfigManager
from dotenv import load_dotenv

class BaseAgent:
    def __init__(self, temperature: float = 0.3, model_name: str = "mixtral-8x7b-32768"):
        # Initialize configuration manager
        self.config = ConfigManager()
        load_dotenv("../.env")  # Adjust path as needed

        self.groq_api_key = os.getenv("GROQ_API_KEY")

        if not self.groq_api_key:
            raise ValueError("❌ GROQ_API_KEY missing from .env file or environment")

        # Configure Groq API
        print(f"BaseAgent initialized from: {os.path.abspath(__file__)}")
        
        # Initialize LLM
        self.llm = ChatGroq(
            temperature=temperature,
            model_name=model_name,
            groq_api_key=self.groq_api_key
        )
        
        # Initialize chain and prompt as None
        self.chain: Optional[Runnable] = None
        self.prompt: Optional[ChatPromptTemplate] = None
    
    def _initialize_chain(self, prompt_template: str):
        """Initialize LangChain with chat prompt template"""
        self.prompt = ChatPromptTemplate.from_messages([
            ("human", prompt_template),
        ])
        self.chain = self.prompt | self.llm
    
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