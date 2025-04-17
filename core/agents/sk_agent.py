from core.adapters.llm_adapter import LLMAdapter
from core.memory.in_memory_adapter import InMemoryAdapter
from core.config.roles import MessageRole

class SKAgent:
    def __init__(self, adapter: LLMAdapter):
        self.adapter = adapter

    @classmethod
    async def create(cls, name: str, system_prompt: str, adapter_class, memory=None, **kwargs):
        adapter = await adapter_class.create(
            name=name,
            system_message=system_prompt,
            memory=memory or InMemoryAdapter(),  # 🧠 Default to InMemory
            **kwargs
        )
        return cls(adapter)

    async def run(self, input_text: str) -> str:
        return await self.adapter.generate_response(input_text)
