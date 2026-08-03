import os
from types import SimpleNamespace

import numpy as np
import pytest
from src.embeddings import SentenceTransformerEmbedder, OpenAIEmbedder
from src.embeddings.embedder import DeepSeeekEmbedder


class DummySentenceTransformer:
    def __init__(self, model_name):
        self.model_name = model_name

    def get_sentence_embedding_dimension(self):
        return 8

    def encode(self, texts, normalize_embeddings=True, batch_size=None, show_progress_bar=None):
        if isinstance(texts, str):
            return np.ones(8)
        return np.vstack([[1.0] * 8 for _ in texts])


class DummyOpenAI:
    class embeddings:
        @staticmethod
        def create(input, model):
            if isinstance(input, str):
                return SimpleNamespace(data=[SimpleNamespace(embedding=[0.1, 0.2, 0.3])])
            return SimpleNamespace(data=[SimpleNamespace(embedding=[0.1, 0.2, 0.3]) for _ in input])

    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key
        self.base_url = base_url


def test_sentence_transformer_embedder_returns_vector_and_metadata(monkeypatch):
    monkeypatch.setattr("src.embeddings.embedder.SentenceTransformer", DummySentenceTransformer)

    embedder = SentenceTransformerEmbedder()
    assert embedder.dimensions == 8

    vector = embedder.embed_one("hello world")
    assert isinstance(vector, list)
    assert len(vector) == 8

    chunks = [{"text": "hello world", "metadata": {}}]
    output = embedder.embed_many(chunks)
    assert output[0]["vector"] == [1.0] * 8


def test_openai_embedder_uses_openai_client(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("src.embeddings.embedder.openai.OpenAI", DummyOpenAI)

    embedder = OpenAIEmbedder()
    vector = embedder.embed_one("query")

    assert vector == [0.1, 0.2, 0.3]
    multipled = embedder.embed_many(["a", "b"])
    assert multipled == [[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]


def test_deepseeek_embedder_caches_dimensions(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr("src.embeddings.embedder.openai.OpenAI", DummyOpenAI)

    embedder = DeepSeeekEmbedder()
    vector = embedder.embed_one("query")

    assert vector == [0.1, 0.2, 0.3]
    assert embedder.dimension == 3
