import os
from autogen import AssistantAgent

class ExecutorAgent(AssistantAgent):
    def __init__(self, name, llm_config, system_message, output_dir="generated_files"):
        super().__init__(name=name, llm_config=llm_config, system_message=system_message)
        self.output_dir = output_dir
        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_file(self, file_name, content):
        """Create a file with the provided name and content."""
        file_path = os.path.join(self.output_dir, file_name)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path

    def process_request(self, request):
        """Handle the request to create a file."""
        # Here, we're expecting a request like {'file_name': 'example.py', 'content': 'print("Hello, world!")'}
        file_name = request.get("file_name")
        content = request.get("content")
        
        if not file_name or not content:
            return "Invalid request. File name and content are required."
        
        file_path = self.create_file(file_name, content)
        return f"File created successfully: {file_path}"

# Example usage:
ollama_config = {
    "temperature": 0.7,
    "config_list": [
        {
            "model": "deepseek-coder",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",  # Dummy value for Ollama
            "price": [0.0, 0.0]
        }
    ]
}

# Create the Executor Agent
executor = ExecutorAgent(
    name="FileExecutor",
    llm_config=ollama_config,
    system_message="You are an agent who creates files based on requests."
)

# Example request to create a Python file
request = {
    "file_name": "example.py",
    "content": 'print("Hello, world!")'
}

# Process the request
response = executor.process_request(request)
print(response)
