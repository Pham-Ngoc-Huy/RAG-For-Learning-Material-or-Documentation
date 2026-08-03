import pytest
from src.chunking import FixedSizeChunker, RecursiveChunker, MarkDownChunker


def test_fixed_size_chunker_splits_with_overlap():
    doc = {"text": "a" * 600, "metadata": {"source": "file"}}
    chunker = FixedSizeChunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk(doc)

    assert len(chunks) == 4
    assert chunks[0]["metadata"]["chunk_index"] == 0
    assert chunks[-1]["metadata"]["chunk_index"] == 3
    assert chunks[-1]["metadata"]["total_chunk"] == 4


def test_recursive_chunker_preserves_sentences():
    text = "Sentence one. Sentence two. Sentence three."
    doc = {"text": text, "metadata": {"source": "file"}}
    chunker = RecursiveChunker(chunk_size=25, chunk_overlap=5)
    chunks = chunker.chunk(doc)

    assert len(chunks) >= 2
    assert any("Sentence one" in item["text"] for item in chunks)
    assert any("Sentence three" in item["text"] for item in chunks)


def test_markdown_chunker_splits_by_header():
    text = "# Section 1\nParagraph one.\n\n## Section 2\nParagraph two.\n"
    doc = {"text": text, "metadata": {"source": "file"}}
    chunker = MarkDownChunker(chunk_size=100, chunk_overlap=10)
    chunks = chunker.chunk(doc)

    assert len(chunks) == 2
    assert "Section 1" in chunks[0]["text"]
    assert "Section 2" in chunks[1]["text"]
    assert chunks[0]["metadata"]["chunk_index"] == 0
    assert chunks[1]["metadata"]["total_chunk"] == 2
