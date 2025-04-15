from core.errors.config_error import ConfigValidationError

class Config:
    MODELS_REQUIRING_BASE_URL = ["ollama", "local", "deepseek-coder"]
    SUPPORTED_MODELS = ["gpt-4", "gpt-3.5-turbo", "ollama", "local", "deepseek-coder"]

    def __init__(
        self,
        model: str = None,
        api_key: str = None,
        base_url: str = None,
        temperature: float = 0.3,
        max_tokens: int = 2048
    ):
        if not api_key:
            raise ConfigValidationError("API key must be provided for LLM config.", type(api_key).__name__, "str")

        if not model:
            raise ConfigValidationError("Model must be provided for LLM config.", type(model).__name__, "str")

        if model.lower() not in self.SUPPORTED_MODELS:
            raise ConfigValidationError(f"Unsupported model '{model}' provided.", type(model).__name__, "Supported model string")

        if not (0 <= temperature <= 1):
            raise ConfigValidationError("Temperature must be between 0 and 1.", type(temperature).__name__, "float")

        if max_tokens <= 0:
            raise ConfigValidationError("max_tokens must be a positive integer.", type(max_tokens).__name__, "int")

        config_entry = {
            "model": model,
            "api_key": api_key,
        }

        if model.lower() in self.MODELS_REQUIRING_BASE_URL:
            if not base_url:
                raise ConfigValidationError(
                    f"base_url is required for model '{model}'.",
                    type(base_url).__name__,
                    "str"
                )
            if not isinstance(base_url, str):
                raise ConfigValidationError("base_url must be a string.", type(base_url).__name__, "str")
            config_entry["base_url"] = base_url

        self.llm_config = {
            "config_list": [config_entry],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

    def get_llm_config(self):
        return self.llm_config

    def get_model(self) -> str:
        return self.llm_config["config_list"][0]["model"]

    def __repr__(self):
        config = self.llm_config["config_list"][0]
        return (
            f"<Config(model={config['model']}, "
            f"base_url={config.get('base_url', 'default')}, "
            f"temperature={self.llm_config['temperature']}, "
            f"max_tokens={self.llm_config['max_tokens']})>"
        )
