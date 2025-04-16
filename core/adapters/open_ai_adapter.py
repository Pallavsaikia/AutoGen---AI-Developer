import logging
import openai
from typing import List, Dict
from core.adapters.llm_adapter import LLMAdapter  # Adjust the import path as needed
from core.config.roles import MessageRole
from core.memory import Memory  # Import the Memory class

logger = logging.getLogger(__name__)

class OpenAIAdapter(LLMAdapter):
    def __init__(self, name: str, system_message: str, token_limit: int = 150, **llm_kwargs):
        """
        Initialize the OpenAIAdapter with hardcoded OpenAI model configuration.

        :param name: Name of the agent.
        :param system_message: System message to set for the AssistantAgent.
        :param token_limit: Maximum number of tokens for the OpenAI API response.
        :param llm_kwargs: Parameters passed as keyword arguments for API key, base_url, temperature, etc.
        """
        # Hardcode the model to "gpt-3.5-turbo" (default)
        llm_kwargs["model"] = llm_kwargs.get("model", "gpt-3.5-turbo")
        self.token_limit = token_limit
        # Call the parent constructor (LLMAdapter)
        super().__init__(name, system_message, **llm_kwargs)

        # Initialize the memory instance
        self.memory = Memory()
        self.memory.add_message(MessageRole.SYSTEM, system_message)
        
    def build_llm_config(self) -> dict:
        """
        Builds the config required for OpenAI API usage.
        """
        return {
            "model": self.llm_kwargs["model"],
            "api_key": self.llm_kwargs["api_key"],  # OpenAI API key
            "temperature": self.llm_kwargs.get("temperature", 0.7),
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
        openai.api_key = self.llm_config["api_key"]

        # Prepare the conversation history with the previous context and the new user message
        # prompt = f"Please provide a detailed response to: {messages[-1]['content']}"
        messages_to_send = self.memory.get_history()  # Use memory for conversation context
        print(f" History : {messages_to_send}")
        try:
            # Make the API call using the OpenAI chat completions method
            api_response = openai.chat.completions.create(
                model=self.llm_config["model"],
                messages=messages_to_send,
                temperature=self.llm_config.get("temperature", 0.7),
                max_tokens=self.token_limit
            )

            # Extract the assistant's reply from the response
            assistant_reply = api_response.choices[0].message.content
            logger.debug(f"[{self.name}] Assistant response: {assistant_reply}")

            # Add the assistant's response to memory
            self.memory.add_message(MessageRole.ASSISTANT, assistant_reply)

            return assistant_reply

        except openai.OpenAIError as e:
            logger.error(f"[{self.name}] OpenAI API request failed: {e}")
            return f"Error: {str(e)}"
        except Exception as e:
            logger.error(f"[{self.name}] OpenAI API Generic request failed: {e}")
            return f"Error: {str(e)}"
