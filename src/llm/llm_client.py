from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    response: str


class BaseLLMClient(ABC):
    """
    @brief Define a reusable contract for LLM interactions.
    @objective Allow different LLM providers (OpenAI, Google, etc.) to be pluggable.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    @abstractmethod
    def generate(
        self,
        prompt: str = "",
        messages: Optional[list[dict]] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """Generate a response from the LLM given a prompt or message history.

        @brief Call the LLM and return structured response.
        @param prompt: the formatted prompt text (usually from a prompt template)
        @param messages: optional chat message history for OpenRouter-style APIs
        @param max_tokens: maximum tokens in the response
        @param temperature: sampling temperature (0.0 = deterministic, 1.0 = creative)
        @return: LLM Response
        @update date 2026-08-07
        @commented by Huy Pham
        """
        pass


class ThinkingFromKnowledgeBase(BaseLLMClient):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = None,
        provider: str = None,
    ):
        self.model = model
        self.provider = provider
        if not api_key:
            raise ValueError("There is no API Key exists")
        self.api_key = api_key

        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def generate(
        self,
        prompt: Optional[str] = None,
        messages: Optional[list[dict]] = None,
        temperature: float = 0.7,
    ) -> LLMResponse:
        # if not prompt or not messages:
        #     raise ValueError("Must provide either `prompt` or `messages`")

        payload_messages = messages or [{"role": "user", "content": prompt}]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=payload_messages,
                temperature=temperature,
            )

            answer_text = response.choices[0].message.content

            return LLMResponse(
                text=answer_text,
                provider=self.provider,
                model=self.model,
                response=response.model_dump(),
            )

        except Exception as e:
            print(f"Error calling {self.provider}: {str(e)}")
            return LLMResponse(
                text=f"Error: {str(e)}",
                provider=self.provider,
                model=self.model,
                response={},
            )
