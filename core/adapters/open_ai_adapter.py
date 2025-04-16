import logging
import os
import openai
from .llm_adapter import LLMAdapter  # Adjust the import path as needed

logger = logging.getLogger(__name__)

class OpenAIAdapter(LLMAdapter):
    def __init__(self, name: str, system_message: str,token_limit: int = 150, **llm_kwargs):
        """
        Initialize the OpenAIAdapter with hardcoded OpenAI model configuration.

        :param name: Name of the agent.
        :param system_message: System message to set for the AssistantAgent.
        :param llm_kwargs: Parameters passed as keyword arguments for API key, base_url, temperature, etc.
        """
        # Hardcode the model to "gpt-3.5-turbo" (default)
        llm_kwargs["model"] = llm_kwargs.get("model", "gpt-3.5-turbo")
        self.token_limit=token_limit
        # Call the parent constructor (LLMAdapter)
        super().__init__(name, system_message, **llm_kwargs)

    def build_llm_config(self) -> dict:
        """
        Builds the config required for OpenAI API usage.
        """
        return {
            "model": self.llm_kwargs["model"],
            "api_key": self.llm_kwargs["api_key"],  # OpenAI API key
            "temperature": self.llm_kwargs.get("temperature", 0.7),
        }

    def generate_response(self, task_description: str,additional_context:str=None) -> str:
        """
        Sends a prompt to the OpenAI model and retrieves the generated response.
        """
        logger.info(f"[{self.name}] Generating response for task: {task_description}")

        # Create the prompt to pass to the model
        prompt = f"Please provide a detailed response to: {task_description}"

        # Configure the OpenAI API client with the API key
        openai.api_key = self.llm_config["api_key"]

        try:
            # Prepare the messages for the request
            messages = [
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": prompt},
               
            ]
            if additional_context:
                messages.append({"role": "assistant", "content": additional_context})
            # Make the API call using the correct chat completions method
            response = openai.chat.completions.create(
                model=self.llm_config["model"],
                messages=messages,
                temperature=self.llm_config.get("temperature", 0.7),
                max_tokens=self.token_limit
            )

            # Return the assistant's reply
            # print(response.model_dump_json())
            return response.choices[0].message.content

        except openai.OpenAIError as e:
            logger.error(f"[{self.name}] OpenAI API request failed: {e}")
            return f"Error: {str(e)}"
        except Exception as  e:
            logger.error(f"[{self.name}] OpenAI API Generic request failed: {e}")
            return f"Error: {str(e)}"