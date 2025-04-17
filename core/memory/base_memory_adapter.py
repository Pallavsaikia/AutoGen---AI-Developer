from abc import ABC, abstractmethod
from typing import List, Dict
from core.config.roles import MessageRole

class BaseMemoryAdapter(ABC):
    async def add_message(self, role: MessageRole, content: str):
        """
        Validates message role and delegates to the subclass implementation.
        """
        if not isinstance(role, MessageRole):
            raise ValueError(f"Invalid message role: {role}. Must be one of {list(MessageRole)}.")
        
        # Delegate to the subclass method for actual handling
        await self._add_message(role, content)

    @abstractmethod
    async def _add_message(self, role: MessageRole, content: str):
        """
        Abstract method that must be implemented by subclasses for actual message handling.
        """
        pass

    @abstractmethod
    async def get_history(self, limit: int = 10) -> List[Dict]:
        pass

    @abstractmethod
    async def clear_history(self):
        pass
