from abc import ABC, abstractmethod

from src.actions.construction import Embedded, QdrantCollection
from src.chunking.chunker import MarkDownChunker
from src.ingestion.loader import FileLoader


class UploadService(ABC):
    @abstractmethod
    async def upload_file(
        self,
        user_id: str,
        user_name: str,
        collection_name: str,
        file_path: str,
        model: str,
    ) -> dict:
        pass


class UploadServiceImpl(UploadService):
    def __init__(self, config):
        self.config = config

    async def upload_file(
        self,
        user_id: str,
        user_name: str,
        collection_name: str,
        file_path: str,
        model: str,
    ) -> dict:
        # Process the file and extract text
        doc_result = FileLoader(file_path=file_path).load()
        if doc_result is None:
            raise ValueError(f"Could not load or extract text from: {file_path}")

        # Split the loaded document into chunks
        chunks = MarkDownChunker().chunk(doc=doc_result)

        # Generate embeddings for the chunks
        embedder = Embedded(
            config=self.config,
            user_id=user_id,
            user_name=user_name,
            model=model,
        )
        chunks = embedder.embed_many(chunks=chunks)

        # Store the embedded chunks into the tenant collection
        collection = QdrantCollection(
            config=self.config,
            user_id=user_id,
            user_name=user_name,
            model=model,
        )
        collection.create(collection_name=collection_name)
        point_ids = collection.upsert(collection_name=collection_name, chunks=chunks)

        return {
            "collection_name": collection_name,
            "total_chunks": len(point_ids),
        }
