from core.adapters import DeepSeekAdapter,OpenAIAdapter
from dotenv import load_dotenv
import os
from core.code_builder import extract_code
# Load variables from .env file
load_dotenv()


deepseek_agent = DeepSeekAdapter(
    name="DeepCoder",
    system_message="You are a Software developer.Only Respond Code back.Dont send additional text other than the code(strict)",
    api_key="my-deepseek-key",
    base_url="http://localhost:11434/v1/chat/completions",
    temperature=0.7
)

task_description = "create python program from scratch to create jwt strings"
response = deepseek_agent.generate_response(task_description)
response = deepseek_agent.generate_response("Donot use JWt lib")
# print(response)
# response = deepseek_agent.generate_response(additional)
print("--------------------------------------------")
print(response)
code=extract_code(response,"python")[0]
# print(type(code))
# print(code)
with open('output.py', 'w', encoding='utf-8') as file:
    file.write(code)


# print(response)
print("-----------------------------------------------------------------------------")
# openai_adapter = OpenAIAdapter(
#     name="OpenAIAgent",
#     system_message="You are a Software developer.Only Respond Code back.Dont send anything other than the code(strict)",
#     api_key=os.getenv("OPEN_AI_API_KEY"),  # Your OpenAI API key here
#     model="gpt-4",  # Optionally override the model to use GPT-4
#     temperature=0.7,
# )

# task_description = "Give me the code to get matrix multiplication.Dont send anything other than the code(strict)"
# additional="remove ```python from response"
# response = openai_adapter.generate_response(task_description)
# print(response)
# response = openai_adapter.generate_response(additional)
# print(response)