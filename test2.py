import logging
import requests
from core.config.base_config import Config
from core.errors.config_error import ConfigValidationError
from core.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class DeveloperAgent(BaseAgent):
    def __init__(self, name: str, system_message: str, api_key: str, base_url: str, temperature: float = 0.3, max_tokens: int = 2048):
        """
        Initialize the DeveloperAgent with the necessary configurations.
        This will extend BaseAgent to include deepseek-coder model specific functionality.
        
        :param api_key: API key for authentication with the LLM API
        :param base_url: URL of the deepseek-coder API endpoint
        :param temperature: The temperature setting for code generation (0.0 to 1.0)
        :param max_tokens: The maximum number of tokens for the response
        """
        # Setup Config with deepseek-coder model
        config = Config(
            model="deepseek-coder",
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Initialize the BaseAgent with the created config
        super().__init__(name=name, system_message=system_message, config=config)

        logger.info(f"DeveloperAgent {name} initialized with deepseek-coder model.")
    
    def developer_action(self):
        """Basic example method to perform a developer-related task."""
        logger.info(f"DeveloperAgent {self.name} is performing a developer action.")
        return "Developer action completed successfully."
    
    def generate_code(self, task_description: str) -> str:
        """
        Sends a prompt to the deepseek-coder model and retrieves the generated code.
        
        :param task_description: A description of the task to generate code for
        :return: The generated code or an error message if something goes wrong
        """
        logger.info(f"Generating code for task: {task_description}")
        
        # Craft the prompt for the task description
        prompt = f"Write only the Python code to {task_description}. Please provide no explanations or additional text."

        # Prepare the request payload
        payload = {
            "model": self.llm_config["config_list"][0]["model"],
            "messages": [
                {
                    "role": "user",  # The role of the person providing the request
                    "content": prompt
                }
            ]
        }

        # Prepare headers for the API request
        headers = {
            "Authorization": f"Bearer {self.llm_config['config_list'][0]['api_key']}",
            "Content-Type": "application/json"
        }

        try:
            # Make the POST request to the deepseek-coder API
            response = requests.post(self.llm_config["config_list"][0]["base_url"], headers=headers, json=payload)
            response.raise_for_status()  # Raise an error if the response status is not successful

            # Extract the response data
            data = response.json()
            generated_code = data["choices"][0]["message"]["content"]
            
            return generated_code.strip()  # Strip any leading or trailing spaces/newlines
        except requests.exceptions.RequestException as e:
            # Handle errors from the API request
            logger.error(f"Error while generating code: {e}")
            return f"Error while generating code: {e}"


# Example usage
if __name__ == "__main__":
    # Set your API key and base URL (adjust according to your setup)
    api_key = "your_api_key_here"
    base_url = "http://localhost:11434/v1/chat/completions"  # Update with your actual deepseek-coder URL

    # Initialize the DeveloperAgent
    agent = DeveloperAgent(
        name="dev-agent-coder-01",
        system_message="I am a developer assistant specialized in code generation.",
        api_key=api_key,
        base_url=base_url
    )
    
    # Define a task description (e.g., asking to generate a Python function to reverse a string)
    task_description = "create a function to reverse a string in Python"

    # Generate code for the task
    generated_code = agent.generate_code(task_description)
    with open('file_name.py', "w") as file:
        file.write(generated_code)
    # Print the generated code
    print("Generated Code:")
    print(generated_code)
