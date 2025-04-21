import logging
import openai
from typing import List, Dict
from core.adapters.llm_adapter import LLMAdapter  # Adjust the import path as needed
from core.config.roles import MessageRole
from core.memory.base_memory_adapter import BaseMemoryAdapter  # Import the Memory class

logger = logging.getLogger(__name__)

class OpenAIAdapter(LLMAdapter):
    @classmethod
    async def create(cls, name: str, system_message: str, memory: BaseMemoryAdapter = None, **llm_kwargs):
        llm_kwargs.setdefault("model", "gpt-4o-mini")
        return await super().create(name=name, system_message=system_message, memory=memory, **llm_kwargs) 
     
    def build_llm_config(self) -> dict:
        """
        Builds the config required for OpenAI API usage.
        """
        return {
            "model": self.llm_kwargs["model"],
            "api_key": self.llm_kwargs["api_key"],  # OpenAI API key
            "temperature": self.llm_kwargs.get("temperature", 0.7),
            "token_limit":self.llm_kwargs.get("token_limit", None),
        }

    def model_request(self, messages_to_send: List[Dict]) -> str:
        # Prepare the OpenAI API client with the API key
        openai.api_key = self.llm_config["api_key"]

        try:
            # Make the API call using the OpenAI chat completions method
            api_response = openai.chat.completions.create(
                model=self.llm_config["model"],
                messages=messages_to_send,
                temperature=self.llm_config.get("temperature", 0.7),
                max_tokens= self.llm_config.get("token_limit")
            )

            # Extract the assistant's reply from the response
            assistant_reply = api_response.choices[0].message.content
            logger.debug(f"[{self.name}] Assistant response: {assistant_reply}")


            return assistant_reply

        except openai.OpenAIError as e:
            logger.error(f"[{self.name}] OpenAI API request failed: {e}")
            return f"Error: {str(e)}"
        except Exception as e:
            logger.error(f"[{self.name}] OpenAI API Generic request failed: {e}")
            return f"Error: {str(e)}"
