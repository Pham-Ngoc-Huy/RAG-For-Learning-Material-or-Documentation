from abc import ABC, abstractmethod
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
import uuid

class BaseVectorStore(ABC):
    