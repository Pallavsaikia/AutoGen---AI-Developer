from typing import List, Dict
from core.config.roles import MessageRole
from core.memory.base_memory_adapter import BaseMemoryAdapter

class InMemoryAdapter(BaseMemoryAdapter):
    def __init__(self, max_history: int = 10):
        """
        Initializes the conversation memory.

        :param max_history: Maximum number of messages to store in memory.
        """
        self.max_history = max_history
        self.messages: List[Dict] = []

    async def _add_message(self, role: MessageRole, content: str):
        """
        Adds a message to memory with strict role validation.
        """
        # Store the message in the in-memory list
        self.messages.append({"role": role.value, "content": content})
        
        # Ensure the memory doesn't exceed the max history
        if len(self.messages) > self.max_history:
            self.messages.pop(0)

    async def get_history(self, limit: int = 10) -> List[Dict]:
        """
        Returns the last N messages from memory.
        """
        return self.messages[-limit:].copy()

    async def clear_history(self):
        """
        Clears the entire message history.
        """
        self.messages.clear()
