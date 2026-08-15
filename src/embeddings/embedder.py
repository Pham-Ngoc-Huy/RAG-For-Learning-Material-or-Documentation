from abc import ABC, abstractmethod
import openai

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

        if self.api_key is None:
            raise ValueError ("This need to API-KEY for model embedding")
        else:
            self.client=openai.OpenAI(base_url=self.base_url, api_key=self.api_key)

    @property
    def get_vectorspace_dimensions(self):
        if self._dimensions is None:
            response = self.client.embeddings.create(input="Hi", model=self.model)
            self._dimensions = len(response.data[0].embedding)
        return self._dimensions
    
    def embed_one(self, text:str):
        response = self.client.embeddings.create(input=text, model=self.model)
        vector = response.data[0].embedding
        return vector                    

    def _batch_embed(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(input=texts, model=self.model)
        vectors = [item.embedding for item in response.data]
        return vectors
