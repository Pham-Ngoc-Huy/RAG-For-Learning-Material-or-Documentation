from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Union
import yaml

class PromptTemplate(ABC):
    """Abstract base class for prompt template implementations.

    @brief Define a reusable prompt formatting contract.
    @objective Allow prompt builders to produce final prompt text from templates.
    @update date 2026-08-07
    @commented by Huy Pham
    """
    @abstractmethod
    def build(self, template_name:str, **kwargs) -> List[Dict[str,str]]:
        """Format the prompt template with provided keyword arguments.

        @brief Build the final prompt text.
        @param kwargs: template variables such as 'query', 'retrieved_chunks', or other prompt fields.
        @return: formatted prompt string.
        """
        pass

class PromptAssistance(PromptTemplate):
    def __init__(self, prompts_dir: Union[str, Path] = "prompts"):
        """
        @brief create PromptAssistance
        @param prompts_dir: template as yml (VD: 'prompts/')
        """
        self.prompts_dir = Path(prompts_dir)
        
        if not self.prompts_dir.exists() or not self.prompts_dir.is_dir():
            raise NotADirectoryError(f"TPrompts Root Not-Found: {self.prompts_dir.absolute()}")

    def _load_yaml(self, template_name: str) -> dict:
        """Read and Parse file YAML """
        
        if not template_name.endswith(('.yml', '.yaml')):
            template_name += '.yaml'
            
        file_path = self.prompts_dir / template_name
        
        if not file_path.exists():
            raise FileNotFoundError(f"Not-Found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise ValueError(f"Syntax error in file YAML '{template_name}': {e}")

    def build(self, template_name: str, **kwargs) -> List[Dict[str, str]]:

        prompt_data = self._load_yaml(template_name)
        messages = []

        if "system_message" in prompt_data and prompt_data["system_message"]:
            system_content = prompt_data["system_message"]
            try:
                system_content = system_content.format(**kwargs)
            except KeyError:
                pass 
            
            messages.append({
                "role": "system",
                "content": system_content.strip()
            })

        if "user_message_template" in prompt_data and prompt_data["user_message_template"]:
            user_template = prompt_data["user_message_template"]
            try:
                user_content = user_template.format(**kwargs)
                messages.append({
                    "role": "user",
                    "content": user_content.strip()
                })
            except KeyError as e:
                raise ValueError(f"Template '{template_name}' missing parameters: {e}")
        else:
            raise ValueError(f"File YAML '{template_name}' must contain 'user_message_template'")

        return messages