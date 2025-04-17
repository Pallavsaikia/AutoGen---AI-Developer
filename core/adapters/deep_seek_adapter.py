from core.adapters.llm_adapter import LLMAdapter
import requests
import logging
from core.memory.base_memory_adapter import BaseMemoryAdapter
from typing import List, Dict

logger = logging.getLogger(__name__)

class DeepSeekAdapter(LLMAdapter):
    @classmethod
    async def create(cls, name: str, system_message: str, memory: BaseMemoryAdapter = None, **llm_kwargs) :
        llm_kwargs.setdefault("model", "deepseek-coder:6.7b")
        return await super().create(name=name, system_message=system_message, memory=memory, **llm_kwargs)

    def build_llm_config(self) -> dict:
        """
        Builds the configuration needed for DeepSeek API usage.
        """
        return {
            "model": self.llm_kwargs["model"],
            "api_key": self.llm_kwargs["api_key"],
            "base_url": self.llm_kwargs["base_url"],
            "temperature": self.llm_kwargs.get("temperature", 0.3),
        }

    def model_request(self, messages_to_send: List[Dict]) -> str:
        """
        Make the request to the DeepSeek API and process the response.
        """
        payload = {
            "model": self.llm_config["model"],
            "temperature": self.llm_config.get("temperature", 0.3),
            "messages": messages_to_send,
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
            return message

        except requests.exceptions.RequestException as e:
            logger.error(f"[{self.name}] DeepSeek API request failed: {e}")
            return f"Error: {str(e)}"
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"[{self.name}] Unexpected DeepSeek response format: {e}")
            return "Error: Unexpected response format from DeepSeek API."

