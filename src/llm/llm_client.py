import json
import os
from abc import ABC, abstractmethod
from typing import Optional

import requests
from openai import OpenAI


class BaseLLMClient(ABC):
    """Abstract base class for LLM client implementations.

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
    ) -> dict:
        """Generate a response from the LLM given a prompt or message history.

        @brief Call the LLM and return structured response.
        @param prompt: the formatted prompt text (usually from a prompt template)
        @param messages: optional chat message history for OpenRouter-style APIs
        @param max_tokens: maximum tokens in the response
        @param temperature: sampling temperature (0.0 = deterministic, 1.0 = creative)
        @return: dict with keys: 'response', 'tokens_used', 'model', 'stop_reason'
        @update date 2026-08-07
        @commented by Huy Pham
        """
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI GPT-based LLM client.

    @brief Call OpenAI models via the OpenAI Python SDK.
    @objective Provide a GPT-3.5/GPT-4 backend for the RAG system.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
    ):
        """Initialize the OpenAI client.

        @brief Set up OpenAI API connection.
        @param api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        @param model: model name to use (default: gpt-3.5-turbo)
        @update date 2026-08-07
        @commented by Huy Pham
        """
        self.model = model
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not provided. Set OPENAI_API_KEY environment variable."
            )
        self.client = OpenAI(api_key=api_key)

    def generate(
        self,
        prompt: str = "",
        messages: Optional[list[dict]] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> dict:
        """Generate a response from OpenAI.

        @brief Call OpenAI API and parse response.
        @param prompt: the full formatted prompt (system + context + query)
        @param messages: optional chat message history to send instead of a one-shot prompt
        @param max_tokens: maximum tokens in the response
        @param temperature: sampling temperature for response diversity
        @return: structured dict with response, token count, and metadata
        @update date 2026-08-07
        @commented by Huy Pham
        """
        if not prompt and not messages:
            return {
                "response": "",
                "tokens_used": 0,
                "model": self.model,
                "stop_reason": "empty_prompt",
            }

        payload_messages = messages or [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=payload_messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            response_text = completion.choices[0].message.content
            tokens_used = (
                completion.usage.prompt_tokens + completion.usage.completion_tokens
            )
            stop_reason = completion.choices[0].finish_reason

            return {
                "response": response_text,
                "tokens_used": tokens_used,
                "model": self.model,
                "stop_reason": stop_reason,
            }
        except Exception as e:
            return {
                "response": f"Error calling OpenAI: {str(e)}",
                "tokens_used": 0,
                "model": self.model,
                "stop_reason": "error",
            }


class DeepSeekClient(BaseLLMClient):
    """DeepSeek LLM client using OpenAI-compatible API.

    @brief Call DeepSeek models via OpenAI-compatible endpoint.
    @objective Provide a DeepSeek backend for the RAG system with cost-effective inference.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "~deepseek/deepseek-v4-flash-latest",
        base_url: str = "https://openrouter.ai/api/v1/chat/completions",
    ):
        """Initialize the DeepSeek client.

        @brief Set up DeepSeek/OpenRouter API connection.
        @param api_key: DeepSeek API key (defaults to DEEPSEEK_API_KEY env var)
        @param model: model name to use (default: ~deepseek/deepseek-v4-flash-latest)
        @param base_url: OpenRouter chat completions endpoint
        @update date 2026-08-07
        @commented by Huy Pham
        """
        self.model = model
        self.base_url = base_url
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "DeepSeek API key not provided. Set DEEPSEEK_API_KEY environment variable."
            )

    def generate(
        self,
        prompt: str = "",
        messages: Optional[list[dict]] = None,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> dict:
        """Generate a response from DeepSeek.

        @brief Call OpenRouter DeepSeek API and parse response.
        @param prompt: the full formatted prompt (system + context + query)
        @param messages: optional chat message history to send instead of a one-shot prompt
        @param max_tokens: maximum tokens in the response
        @param temperature: sampling temperature for response diversity
        @return: structured dict with response, token count, and metadata
        @update date 2026-08-07
        @commented by Huy Pham
        """
        if not prompt and not messages:
            return {
                "response": "",
                "tokens_used": 0,
                "model": self.model,
                "stop_reason": "empty_prompt",
            }

        payload_messages = messages or [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": payload_messages,
            "reasoning": {"enabled": True},
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                url=self.base_url,
                headers=headers,
                data=json.dumps(payload),
                timeout=30,
            )
            response.raise_for_status()
            body = response.json()
            message = body["choices"][0]["message"]
            response_text = message.get("content", "")
            reasoning_details = message.get("reasoning_details")
            usage = body.get("usage", {})
            tokens_used = usage.get("total_tokens", 0)
            stop_reason = body["choices"][0].get("finish_reason")

            return {
                "response": response_text,
                "tokens_used": tokens_used,
                "model": self.model,
                "stop_reason": stop_reason,
                "reasoning_details": reasoning_details,
            }
        except Exception as e:
            return {
                "response": f"Error calling DeepSeek: {str(e)}",
                "tokens_used": 0,
                "model": self.model,
                "stop_reason": "error",
            }


class LocalLLMClient(BaseLLMClient):
    """Mock LLM client for testing without API calls.

    @brief Provide a stub LLM that returns predictable responses.
    @objective Enable testing the full pipeline without external API dependencies.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    def __init__(self, model: str = "local-mock"):
        """Initialize the local mock client.

        @param model: model name for logging purposes
        """
        self.model = model

    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> dict:
        """Return a mock response for testing.

        @brief Generate a stub response based on the prompt.
        @param prompt: the prompt text (used to generate mock response)
        @param max_tokens: max tokens (for mock calculation)
        @param temperature: temperature (ignored in mock)
        @return: mock response dict
        """
        # Simple mock: count questions in prompt and respond accordingly
        question_mark_count = prompt.count("?")
        if question_mark_count > 0:
            mock_response = (
                f"Based on the provided context, I can answer this question. "
                f"The retrieved documents contained relevant information about the topic. "
                f"(This is a mock response from {self.model} for testing purposes.)"
            )
        else:
            mock_response = "Please ask a clear question about the documents."

        return {
            "response": mock_response,
            "tokens_used": len(mock_response.split()),
            "model": self.model,
            "stop_reason": "max_tokens",
        }
