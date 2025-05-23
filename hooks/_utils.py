import os
import yaml
import pathlib as pl
from enum import Enum


class AIChecksSupportedModels(Enum):
    GEMINI_2_0_FLASH = "gemini-2.0-flash"


class AIChecksConfig:
    def __init__(
        self, config_path: pl.Path = pl.Path(".pre-commit-ai-checks-config.yaml")
    ):
        self.config_path = config_path
        self.ai_model: AIChecksSupportedModels | None = None
        self.api_key: str | None = None
        self.load()

    def load(self):
        if os.getenv("PRE_COMMIT_AI_CHECKS_AI_MODEL") and os.getenv(
            "PRE_COMMIT_AI_CHECKS_API_KEY"
        ):
            self.ai_model = AIChecksSupportedModels(
                os.getenv("PRE_COMMIT_AI_CHECKS_AI_MODEL")
            )
            self.api_key = os.getenv("PRE_COMMIT_AI_CHECKS_API_KEY")
        else:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
                self.ai_model = AIChecksSupportedModels(config.get("ai_model"))
                api_key_raw = config.get("api_key")

                # Handle environment variable references in the API key, e.g. ${PRE_COMMIT_AI_CHECKS_API_KEY}
                if (
                    api_key_raw
                    and isinstance(api_key_raw, str)
                    and api_key_raw.startswith("${")
                    and api_key_raw.endswith("}")
                ):
                    if len(api_key_raw) <= 3:
                        raise ValueError(
                            "Invalid API key: must be a string starting with ${ and ending with }"
                        )

                    env_var = api_key_raw.removeprefix("${").removesuffix("}")
                    self.api_key = os.getenv(env_var)
                else:
                    self.api_key = api_key_raw

        if not self.ai_model or not self.api_key:
            raise ValueError("AI checks pre-commit config is not set")

    def __str__(self):
        return f"AIChecksConfig(ai_model={self.ai_model}, api_key={'*' * len(self.api_key) if self.api_key else 'not specified'})"

    def __repr__(self):
        return self.__str__()
