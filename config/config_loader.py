from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from omegaconf import DictConfig, OmegaConf

class ConfigConstructor(ABC):
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)

    @abstractmethod
    def load(self, **override: Any) -> DictConfig:
        """Load configuration."""
        pass

class OmegaConfigLoader(ConfigConstructor):
    def load(self, **override: Any) -> DictConfig:
        config = OmegaConf.load(self.config_path)
        if override:
            override_config = OmegaConf.create(override)
            config = OmegaConf.merge(config, override_config)
        return config