from core.config.roles import MessageRole

class Memory:
    def __init__(self, max_history: int = 10):
        """
        Initializes the conversation memory.

        :param max_history: Maximum number of messages to store in memory.
        """
        self.max_history = max_history
        self.messages = []

    def add_message(self, role: MessageRole, content: str):
        """
        Adds a message to the conversation memory. Enforces strict message roles.

        :param role: The role of the message sender (must be one of the values from MessageRole).
        :param content: The content of the message.
        """
        if not isinstance(role, MessageRole):
            raise ValueError(f"Invalid message role: {role}. Must be one of {list(MessageRole)}.")
        
        self.messages.append({"role": role.value, "content": content})

        if len(self.messages) > self.max_history:
            self.messages.pop(0)  # Remove the oldest message if history exceeds max limit

    def get_history(self) -> list:
        """
        Returns the conversation history.

        :return: List of message dictionaries.
        """
        return self.messages.copy()

    def clear_history(self):
        """Clears the conversation history."""
        self.messages = []
