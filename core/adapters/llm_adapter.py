import logging
from abc import ABC, abstractmethod
from core.models import ModelPreferences
from typing import List, Dict, Type, TypeVar
from core.config.roles import MessageRole
from core.memory.base_memory_adapter import BaseMemoryAdapter
from core.memory.in_memory_adapter import InMemoryAdapter

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="LLMAdapter")

class LLMAdapter(ABC):
    """
    Abstract base for adapting different LLM providers into AssistantAgent.
    Subclasses must implement `build_llm_config()` and `model_request()`.
    """

    def __init__(self):
        """Prevent usage. Use create() instead."""
        raise RuntimeError("Use `await YourAdapter.create(...)` to instantiate.")


    
    @classmethod
    async def create(cls: Type[T], name: str, system_message: str, memory: BaseMemoryAdapter = None, **llm_kwargs) -> T:
        """
        Async factory method to fully construct and initialize the adapter.
        """
        # Bypass __init__ by manually creating an uninitialized instance
        self: T = object.__new__(cls)

        self.name = name
        self.system_message = system_message
        self.llm_kwargs = llm_kwargs
        self.memory = memory or InMemoryAdapter()

        logger.debug(f"Initializing LLMAdapter: name={self.name}, params={self.llm_kwargs}")

        self._validate_llm_kwargs()

        self.llm_config = self.build_llm_config()
        if not self.llm_config or not isinstance(self.llm_config, dict):
            raise ValueError("LLM config must be a valid dictionary.")

        # self._agent = AssistantAgent(
        #     name=self.name,
        #     system_message=self.system_message,
        #     llm_config=self.llm_config
        # )

        # Asynchronously add the system message to memory
        await self.memory.add_message(MessageRole.SYSTEM, self.system_message)

        return self

    def _validate_llm_kwargs(self):
        model = self.llm_kwargs.get("model")
        api_key = self.llm_kwargs.get("api_key")
        base_url = self.llm_kwargs.get("base_url")
        token_limit = self.llm_kwargs.get("token_limit")
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
    def model_request(self, messages_to_send: List[Dict]) -> str:
        pass

    async def generate_response(self, instructions: str) -> str:
        await self.memory.add_message(MessageRole.USER, instructions)
        messages_to_send = await self.memory.get_history()
        print(messages_to_send)
        message = self.model_request(messages_to_send)
        await self.memory.add_message(MessageRole.ASSISTANT, message)
        return message

    # @property
    # def agent(self) -> AssistantAgent:
    #     return self._agent

    def __repr__(self):
        return f"<LLMAdapter name={self.name}, model={self.llm_config.get('model')}>"
