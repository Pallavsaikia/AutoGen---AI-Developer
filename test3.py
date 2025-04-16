from core.adapters import DeepSeekAdapter,OpenAIAdapter
from dotenv import load_dotenv
import os
# Load variables from .env file
load_dotenv()

deepseek_agent = DeepSeekAdapter(
    name="DeepCoder",
    system_message="You are a Software developer.Only Respond Code back.Dont send additional text other than the code(strict)",
    api_key="my-deepseek-key",
    base_url="http://localhost:11434/v1/chat/completions",
    temperature=0.3
)

task_description = "Give me the code to get matrix multiplication in a class function"
additional="Okay i will only send the code"
response = deepseek_agent.generate_response(task_description,additional)
with open("output.py", "w") as file:
    file.write(response)

print(response)
print("-----------------------------------------------------------------------------")
openai_adapter = OpenAIAdapter(
    name="OpenAIAgent",
    system_message="You are a Software developer.Only Respond Code back.Dont send anything other than the code(strict)",
    api_key=os.getenv("OPEN_AI_API_KEY"),  # Your OpenAI API key here
    model="gpt-4",  # Optionally override the model to use GPT-4
    temperature=0.7,
)

task_description = "Give me the code to get matrix multiplication.Dont send anything other than the code(strict)"
additional="Sure i will only send code back with the ```python"
response = openai_adapter.generate_response(task_description,additional)
print(response)