from abc import ABC, abstractmethod

from config import OmegaConfigLoader


class ReadConfig(ABC):
    @abstractmethod
    async def load_model(self):
        pass


class SelectionModel(ReadConfig):
    config_path = "config/config.yml"

    def __init__(self, model_selection: str):
        self.config = OmegaConfigLoader(config_path=self.config_path).load()
        self.model_available = [key for key, _ in self.config["models"].items()]
        self.model_selection = model_selection

    async def load_model(self):
        if self.model_selection not in self.model_available:
            return None
        else:
            return self.model_selection
