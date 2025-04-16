from core.adapters.llm_adapter import LLMAdapter
import requests
import logging

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
        llm_kwargs["model"] = "deepseek-coder"
        
        # Call the parent constructor (LLMAdapter)
        super().__init__(name, system_message, **llm_kwargs)

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

    def generate_response(self, task_description: str,additional_context:str=None) -> str:
        """
        Sends a prompt to the DeepSeek Coder model and retrieves the generated code.
        """
        logger.info(f"[{self.name}] Generating code for task: {task_description}")

        prompt = f"Write only the Python code to {task_description}. Please provide no explanations or additional text."
        messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "system",
                    "content": self.system_message
                }
            ]
        if additional_context:
            messages.append({"role": "assistant", "content": additional_context}) 
        payload = {
            "model": self.llm_config["model"],
            "temperature": self.llm_config.get("temperature", 0.3),
            "messages": messages
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
                timeout=30
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