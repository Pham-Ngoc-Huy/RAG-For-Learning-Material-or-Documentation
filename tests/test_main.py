import os
import runpy
from pathlib import Path


def test_main_pipeline_runs_with_patched_components(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "temp").mkdir()
    (tmp_path / "temp" / "VGU ATHF PS 1.pdf").write_text("dummy", encoding="utf-8")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fake_load(self):
        return {
            "text": "hello world",
            "metadata": {
                "source": self.file_path.name,
                "file_path": str(self.file_path),
                "file_type": self.file_path.suffix.lstrip("."),
            },
        }

    def fake_chunk(self, doc):
        return [{"text": "chunk text", "metadata": {"chunk_index": 0, "total_chunk": 1}}]

    def fake_embed_many(self, chunks):
        for chunk in chunks:
            chunk["vector"] = [0.1, 0.2]
        return chunks

    monkeypatch.setattr("src.ingestion.loader.FileLoader.load", fake_load)
    monkeypatch.setattr("src.chunking.chunker.MarkDownChunker.chunk", fake_chunk)
    monkeypatch.setattr("src.embeddings.embedder.SentenceTransformerEmbedder.embed_many", fake_embed_many)

    repo_root = Path(__file__).resolve().parents[1]
    result = runpy.run_path(str(repo_root / "main.py"), run_name="__main__")

    assert "chunks" in result
    assert result["chunks"][0]["vector"] == [0.1, 0.2]
