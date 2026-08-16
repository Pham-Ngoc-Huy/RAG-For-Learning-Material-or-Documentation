from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Union
from config.config_loader import NormalLoader

class PromptTemplate(ABC):
    """Abstract base class for prompt template implementations.

    @brief Define a reusable prompt formatting contract.
    @objective Allow prompt builders to produce final prompt text from templates.
    @update date 2026-08-07
    @commented by Huy Pham
    """
    @abstractmethod
    def build(
        self, 
        template_name:str, 
        **kwargs
    ) -> List[Dict[str,str]]:
        """Format the prompt template with provided keyword arguments.

        @brief Build the final prompt text.
        @param kwargs: template variables such as 'query', 'retrieved_chunks', or other prompt fields.
        @return: formatted prompt string.
        """
        pass

class PromptAssistance(PromptTemplate):
    def __init__(
        self, 
        prompts_dir: Union[str, Path] = "src/prompts"
    ):
        """
        @brief create PromptAssistance
        @param prompts_dir: template as yml (VD: 'prompts/')
        """
        self.prompts_dir = Path(prompts_dir)
        
        if not self.prompts_dir.exists() or not self.prompts_dir.is_dir():
            raise NotADirectoryError(f"TPrompts Root Not-Found: {self.prompts_dir.absolute()}")

    def build(
        self, 
        template_name: str, 
        **kwargs
    ) -> List[Dict[str, str]]:

        prompt_data = NormalLoader(config_path=f"src/prompts/{template_name}.yml").load()
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