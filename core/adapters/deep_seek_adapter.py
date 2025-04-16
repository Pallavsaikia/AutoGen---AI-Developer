from core.adapters.llm_adapter import LLMAdapter
import requests
import logging
from core.memory import Memory  
from core.config.roles import MessageRole

logger = logging.getLogger(__name__)

class DeepSeekAdapter(LLMAdapter):
    def __init__(self, name: str, system_message: str, **llm_kwargs):
        """
        Initialize the DeepSeekAdapter with hardcoded model configuration.

        :param name: Name of the agent.
        :param system_message: System message to set for the AssistantAgent.
        :param llm_kwargs: Parameters passed as keyword arguments for API key, base_url, temperature, etc.
        """
        # Hardcode the model to "deepseek-coder"
        llm_kwargs["model"] = "deepseek-coder:6.7b"
        
        # Call the parent constructor (LLMAdapter)
        super().__init__(name, system_message, **llm_kwargs)
        
        self.memory = Memory()
        self.memory.add_message(MessageRole.SYSTEM, system_message)

    def build_llm_config(self) -> dict:
        """
        Builds the config required for DeepSeek API usage.
        """
        return {
            "model": self.llm_kwargs["model"],
            "api_key": self.llm_kwargs["api_key"],
            "base_url": self.llm_kwargs["base_url"],
            "temperature": self.llm_kwargs.get("temperature", 0.3),
        }

    def generate_response(self, instructions:str) -> str:
        """
        Sends a prompt to the OpenAI model and retrieves the generated response.
        The method calls the parent `generate_response` method to handle validation and memory management.
        """
        logger.info(f"[{self.name}] Generating response for task.")
        # Call the parent generate_response method to validate messages and update memory
        # self._validate_message_structure(messages)  # Calling the parent method to validate the message structure

        # Add messages to memory before sending them to the model
        
        self.memory.add_message(MessageRole.USER, instructions)

        # Prepare the OpenAI API client with the API key

        # Prepare the conversation history with the previous context and the new user message
        # prompt = f"Please provide a detailed response to: {messages[-1]['content']}"
        messages_to_send = self.memory.get_history()  
        print(messages_to_send)
        payload = {
            "model": self.llm_config["model"],
            "temperature": self.llm_config.get("temperature", 0.3),
            "messages": messages_to_send
        }

        headers = {
            "Authorization": f"Bearer {self.llm_config['api_key']}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                url=self.llm_config["base_url"],
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()

            message = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if not message:
                logger.warning(f"[{self.name}] Empty content returned from DeepSeek.")
                return "No content returned by the model."
            self.memory.add_message(MessageRole.ASSISTANT, message)
            return message

        except requests.exceptions.RequestException as e:
            logger.error(f"[{self.name}] DeepSeek API request failed: {e}")
            return f"Error: {str(e)}"

        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"[{self.name}] Unexpected DeepSeek response format: {e}")
            return "Error: Unexpected response format from DeepSeek API."