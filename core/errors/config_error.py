class ConfigValidationError(Exception):
    def __init__(self, message: str, config_type: str, expected_type: str):
        self.message = message
        self.config_type = config_type
        self.expected_type = expected_type
        super().__init__(self.message)

    def __str__(self):
        return (f"{self.message}\n"
                f"Received config type: {self.config_type}\n"
                f"Expected config type: {self.expected_type}")