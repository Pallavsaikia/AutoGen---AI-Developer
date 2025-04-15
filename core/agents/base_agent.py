import logging
from autogen import AssistantAgent
from core.config.base_config import Config
from core.errors.config_error import ConfigValidationError

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str, system_message: str, config: Config):
        if not isinstance(config, Config):
            raise ConfigValidationError(
                message="Invalid config type passed to BaseAgent.",
                config_type=type(config).__name__,
                expected_type="Config"
            )

        llm_config = config.get_llm_config()

        if not llm_config or not isinstance(llm_config, dict):
            raise ConfigValidationError(
                message="LLM config is empty or invalid. Please check your Config setup.",
                config_type=str(type(llm_config)),
                expected_type="dict"
            )

        self.name: str = name
        self.system_message: str = system_message
        self.llm_config: dict = llm_config

        logger.debug(f"Initializing AssistantAgent: name={self.name}, model={config.get_model()}")

        self._agent: AssistantAgent = AssistantAgent(
            name=self.name,
            system_message=self.system_message,
            llm_config=self.llm_config
        )

    @property
    def agent(self) -> AssistantAgent:
        """Returns the internal AssistantAgent instance."""
        return self._agent
