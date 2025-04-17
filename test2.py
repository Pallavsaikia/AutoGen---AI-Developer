from core.agents.sk_agent import SKAgent
from core.adapters.deep_seek_adapter import DeepSeekAdapter
from core.adapters.open_ai_adapter import OpenAIAdapter
from core.orchestrator.orchestrator import Orchestrator
from dotenv import load_dotenv
import os
# Load variables from .env file
load_dotenv()

# System prompts for each agent role
ROUTER_PROMPT = "You are a routing agent. Based on the input, decide whether it needs coding, verification, or execution."
DEV_PROMPT = "You are a developer. Given a task, write clean and functional Python code."
VERIFIER_PROMPT = "You are a code reviewer. Review the code and return 'APPROVED' or 'REJECTED' with reasons."
EXECUTOR_PROMPT = "You are an executor. If the code is approved, save it and confirm."

async def create_agents():
    # Create agents asynchronously
    router = await SKAgent.create(
        "Router",
        ROUTER_PROMPT,
        OpenAIAdapter,
        api_key=os.getenv("OPEN_AI_API_KEY")
    )

    developer = await SKAgent.create(
        "Developer",
        DEV_PROMPT,
        DeepSeekAdapter,
        api_key="your-deepseek-api-key",
        base_url="http://localhost:11434/v1/chat/completions"  # ✅ required for DeepSeek
    )

    verifier = await SKAgent.create(
        "Verifier",
        VERIFIER_PROMPT,
        OpenAIAdapter,
        api_key=os.getenv("OPEN_AI_API_KEY")
    )

    # Optional executor agent
    # executor = await SKAgent.create(
    #     "Executor",
    #     EXECUTOR_PROMPT,
    #     OpenAIAdapter,
    #     api_key="your-openai-api-key"
    # )
    
    return router, developer, verifier

# To call the function
# agents = await create_agents()  # Uncomment this to call the function asynchronously
async def run_task():
    # Initialize the agents
    router, developer, verifier = await create_agents()

    # Initialize the orchestrator with the agents
    orchestrator = Orchestrator(router, developer, verifier)

    # Example input for task
    input_task = "Write a function that returns the sum of two numbers."
    
    # Run the orchestration
    result = await orchestrator.route_task(input_task)
    print(result)
import asyncio  
if __name__ == "__main__":
    asyncio.run(run_task())