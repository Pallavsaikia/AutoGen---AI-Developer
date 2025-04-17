from core.adapters import DeepSeekAdapter,OpenAIAdapter
from dotenv import load_dotenv
import os
from core.code_builder import extract_code
import asyncio
from core.memory.in_memory_adapter import InMemoryAdapter
# Load variables from .env file
load_dotenv()

# agent = OpenAIAdapter(
#     name="OpenAIAgent",
#     system_message="You are a Software developer.Only Respond Code back.Dont send anything other than the code(strict)",
#     api_key=os.getenv("OPEN_AI_API_KEY"),  # Your OpenAI API key here
#     model="gpt-4",  # Optionally override the model to use GPT-4
#     token_limit=300,
#     temperature=0.7,
# )

# agent = await OpenAIAdapter.create(
#         name="DeepCoder",
#         system_message="You are a Software developer.Only Respond Code back.Dont send additional text other than the code(strict)",
#         memory=InMemoryAdapter(),
#         api_key="my-deepseek-key",
#         base_url="http://localhost:11434/v1/chat/completions",
#         temperature=0.7
#     )

async def run_task():
    # Properly await the async initializer
    # await agent.initialize()
  
    agent = await OpenAIAdapter.create(
        name="OpenAIAgent",
        system_message="You are a Software developer.Only Respond Code back.Dont send anything other than the code(strict)",
        api_key=os.getenv("OPEN_AI_API_KEY"),  # Your OpenAI API key here
        model="gpt-4",  # Optionally override the model to use GPT-4
        temperature=0.7,
    )

    # First Task
    task_description = "Create a Python program from scratch to generate JWT strings"
    response = await agent.generate_response(task_description)
    # print("\nFirst response:\n", response)

    # Second Task
    follow_up = "Do not use any JWT libraries"
    response = await agent.generate_response(follow_up)
    # print("\nSecond response:\n", response)

    # Extract code from response
    code = extract_code(response, "python")
    if code:
        # print(f"\nExtracted {len(code)} code block(s). Writing to output.py...\n")
        with open("output.py", "w", encoding="utf-8") as file:
            file.write(code[0])
        print(code[0])
    else:
        print("\n⚠️ No Python code blocks found in the response.")

# Run the async logic
if __name__ == "__main__":
    asyncio.run(run_task())