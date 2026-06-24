from src.ingestion import FileLoader, DirectoryLoader, URLLoader
from src.chunking import MarkDownChunker, FixedSizeChunker, RecursiveChunker
from src.embeddings import SentenceTransformerEmbedder, OpenAIEmbedder

docs  = FileLoader("temp/VGU ATHF PS 1.pdf").load()
chunks = MarkDownChunker().chunk(doc=docs)
embedder = SentenceTransformerEmbedder()
chunks = embedder.embed_many(chunks)
