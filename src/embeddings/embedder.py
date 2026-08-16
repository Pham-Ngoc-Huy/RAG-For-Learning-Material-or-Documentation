from abc import ABC, abstractmethod
import openai
from sentence_transformers import SentenceTransformer

class BaseEmbedder(ABC):
    @abstractmethod
    def embed_one(
        self, 
        text: str
    ) -> list[float]:
        """Embed a single string -> vector"""
        pass

    @property
    @abstractmethod
    def get_vectorspace_dimensions(self) -> int:
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

class ModelEmbedder(BaseEmbedder):
    def __init__(
        self,
        model:str=None,
        base_url:str=None,
        api_key:str=None
    ):
        self.model = model
        self.base_url = base_url
        self.api_key = api_key

        self._dimensions = None

        if base_url == "local":
            self.client = SentenceTransformer(model)
            self.is_local = True
        else:
            actual_api_key = self.api_key
            if self.api_key is None:
                print("Warning: API Key is missing. Using dummy key 'not-needed' for OpenAI SDK compatibility.")
                actual_api_key = "not-needed"
            self.client = openai.OpenAI(
                base_url=self.base_url, 
                api_key=actual_api_key
            )
            self.is_local = False

    @property
    def get_vectorspace_dimensions(self):
        if self._dimensions is None:
            if self.is_local:
                embedding = self.client.encode("Hi")
                self._dimensions = len(embedding)
            else:
                response = self.client.embeddings.create(input="Hi", model=self.model)
                self._dimensions = len(response.data[0].embedding)
        return self._dimensions
    
    def embed_one(self, text:str):
        if self.is_local:
            return self.client.encode(text).tolist()
        else:
            response = self.client.embeddings.create(input=text, model=self.model)
            return response.data[0].embedding

    def _batch_embed(self, texts: list[str]) -> list[list[float]]:
        if self.is_local:
            embeddings = self.client.encode(texts)
            return embeddings.tolist()
        else:
            response = self.client.embeddings.create(input=texts, model=self.model)
            vectors = [item.embedding for item in response.data]
            return vectors
