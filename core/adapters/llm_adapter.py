import logging
from abc import ABC, abstractmethod
from autogen import AssistantAgent
from core.models import ModelPreferences
from typing import List, Dict
from core.config.roles import MessageRole
logger = logging.getLogger(__name__)




class LLMAdapter(ABC):
    """
    Abstract base for adapting different LLM providers into AssistantAgent.
    Subclasses must implement `build_llm_config()` and `generate_response()` using passed-in parameters.
    """

    

    def __init__(self, name: str, system_message: str, **llm_kwargs):
        self.name: str = name
        self.system_message: str = system_message
        self.llm_kwargs: dict = llm_kwargs
        self.llm_config: dict = {}

        logger.debug(f"Initializing LLMAdapter: name={self.name}, params={self.llm_kwargs}")

        self._validate_llm_kwargs()
        self._agent: AssistantAgent = self._initialize_agent()

    def _validate_llm_kwargs(self):
        model = self.llm_kwargs.get("model")
        api_key = self.llm_kwargs.get("api_key")
        base_url = self.llm_kwargs.get("base_url")

        if not model:
            raise ValueError("Missing required LLM config: 'model' is required.")

        if not any(model.startswith(prefix) for prefix in ModelPreferences.VALID_MODEL_PREFIXES):
            raise ValueError(f"Unsupported model '{model}'. Supported models must start with one of: {ModelPreferences.VALID_MODEL_PREFIXES}")

        if not api_key:
            raise ValueError("Missing required LLM config: 'api_key' is required.")

        if model.startswith("deepseek") and not base_url:
            raise ValueError("Missing required LLM config: 'base_url' is required for DeepSeek models.")

        logger.debug("LLM config parameters validated successfully.")

    @abstractmethod
    def build_llm_config(self) -> dict:
        pass
    
    
     
        
    @abstractmethod
    def generate_response(self, instructions:str) -> str:
        pass

    def _initialize_agent(self) -> AssistantAgent:
        self.llm_config = self.build_llm_config()

        if not self.llm_config or not isinstance(self.llm_config, dict):
            raise ValueError("LLM config must be a valid dictionary.")

        logger.debug(f"Creating AssistantAgent: name={self.name}, model={self.llm_config.get('model')}")
        return AssistantAgent(
            name=self.name,
            system_message=self.system_message,
            llm_config=self.llm_config
        )

    @property
    def agent(self) -> AssistantAgent:
        return self._agent

    def __repr__(self):
        return f"<LLMAdapter name={self.name}, model={self.llm_config.get('model')}>"
