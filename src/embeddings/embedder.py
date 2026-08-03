from abc import ABC, abstractmethod
from typing import Optional
from sentence_transformers import SentenceTransformer
import openai
import os
import numpy as np

class BaseEmbedder(ABC):
    @abstractmethod
    def embed_one(
        self, 
        text: str
    ) -> list[float]:
        """Embed a single string -> vector"""
        pass

    def _batch_embed(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """
        Default: embed one by one. Subclasses can override for true batching.
        """
        return [self.embed_one(t) for t in texts]
    
    def embed_many(
        self,
        chunks: list[dict]
    ) -> list[dict]:
        """
        Embed a user query string
        Seperate method - some models use different
        instructions for queries vs documents
        """
        texts = [chunk["text"] for chunk in chunks]
        vectors = self._batch_embed(texts)

        for chunk, vector in zip(chunks, vectors):
            chunk["vector"] = vector

        return chunks

    def embed_query(
        self,
        query:str
    ) -> list[float]:
        """
        Embed a user query string.
        Separate method - some models use different
        instructions for queries vs documents
        """
        return self.embed_one(query)

class SentenceTransformerEmbedder(BaseEmbedder):
    DEFAULT_MODEL = "all-MiniLM-L6-v2"

    def __init__(
        self,
        model_name:str = DEFAULT_MODEL
    ):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.dimensions = self.model.get_sentence_embedding_dimension()

    def embed_one(
        self,
        text:str
    ) -> list[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def _batch_embed(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=True
        )
        return [v.tolist() for v in vectors]

class OpenAIEmbedder(BaseEmbedder):
    DEFAULT_MODEL = "text-embedding-3-small"
    def __init__(
        self,
        model_name:str = DEFAULT_MODEL
    ):
        self.client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model_name = model_name
        self.dimensions = 1536

    def embed_one(
        self,
        text:str
    ) -> list[float]:
        response = self.client.embeddings.create(
            input=text,
            model=self.model_name
        )
        return response.data[0].embedding

    def embed_many(
        self,
        texts:list[str]
    ) -> list[list[float]]:
        """OpenAI accepts up to 2048 inputs per request"""
        response = self.client.embeddings.create(
            input=texts,
            model=self.model_name
        )
        return [item.embedding for item in response.data]

class DeepSeeekEmbedder(BaseEmbedder):
    """
    Embedder backed by an OpenAI-compatible endpoint (e.g. opencode.ai/zen).

    The zen proxy exposes /v1/embeddings alongside /v1/chat/completions, so
    we strip the trailing path from the URL you were given and let the openai
    client handle routing.

    If the proxy does NOT support /v1/embeddings you'll get a 404 and should
    fall back to SentenceTransformerEmbedder for embeddings and reserve
    DeepSeek for generation only.

    Dimensions: deepseek-v4-flash does not publish a fixed embedding size, so
    we discover it lazily on the first call and cache it.
    """
    BASE_URL= "https://opencode.ai/zen/v1"
    DEFAULT_MODEL = "deepseek-v4-flash-free"

    def __init__(
        self,
        model_name:str = DEFAULT_MODEL,
        base_url:str = BASE_URL,
        api_key:Optional[str] = None,
    ):
        resolved_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "placeholder")
        self.client = openai.OpenAI(api_key=resolved_key, base_url=base_url)
        self.model_name = model_name
        self._dimensions: Optional[int] = None  # discovered on first embed

    @property
    def dimension(self) -> Optional[int]:
        return self._dimensions

    def embed_one(
        self,
        text:str
    ) -> list[float]:
        response = self.client.embeddings.create(input=text, model=self.model_name)
        vector = response.data[0].embedding
        if self._dimensions is None:
            self._dimensions = len(vector)
        return vector

    def _batch_embed(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(input=texts, model=self.model_name)
        vectors = [item.embedding for item in response.data]
        if self._dimensions is None and vectors:
            self._dimensions = len(vectors[0])
        return vectors
