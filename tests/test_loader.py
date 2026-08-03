import os
from pathlib import Path
from types import SimpleNamespace

import pytest
from src.ingestion import FileLoader, DirectoryLoader, URLLoader


def test_file_loader_writes_markdown(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "md_store").mkdir()

    text_file = tmp_path / "doc.txt"
    text_file.write_text("dummy content", encoding="utf-8")

    class DummyResult(SimpleNamespace):
        pass

    dummy_result = DummyResult(text_content="hello world", markdown="# Hello\nworld")
    monkeypatch.setattr("src.ingestion.loader.mid.convert", lambda _: dummy_result)

    loader = FileLoader(str(text_file))
    result = loader.load()

    assert result["text"] == "hello world"
    assert result["metadata"]["source"] == "doc.txt"
    assert result["metadata"]["file_type"] == "txt"
    assert (tmp_path / "md_store" / "doc.md").exists()


def test_file_loader_unsupported_extension(tmp_path):
    file_path = tmp_path / "file.exe"
    file_path.write_text("dummy", encoding="utf-8")
    loader = FileLoader(str(file_path))

    with pytest.raises(ValueError, match="Unsupported type"):
        loader.load()


def test_file_loader_missing_file(tmp_path):
    loader = FileLoader(str(tmp_path / "missing.txt"))

    with pytest.raises(FileNotFoundError):
        loader.load()


def test_url_loader_returns_text_and_metadata(monkeypatch):
    class DummyResult(SimpleNamespace):
        pass

    dummy_result = DummyResult(text_content="page text", markdown="<p>page</p>")
    monkeypatch.setattr("src.ingestion.loader.mid.convert", lambda _: dummy_result)

    loader = URLLoader("https://example.com")
    result = loader.load()

    assert result["text"] == "page text"
    assert result["metadata"]["source"] == "https://example.com"
    assert result["metadata"]["file_type"] == "url"


def test_directory_loader_loads_all_supported_files(tmp_path, monkeypatch):
    directory = tmp_path / "docs"
    directory.mkdir()
    (directory / "a.txt").write_text("a", encoding="utf-8")
    (directory / "b.txt").write_text("b", encoding="utf-8")

    def fake_file_load(self):
        return {
            "text": f"text {self.file_path.name}",
            "metadata": {
                "source": self.file_path.name,
                "file_path": str(self.file_path),
                "file_type": self.file_path.suffix.lstrip("."),
            },
        }

    monkeypatch.setattr("src.ingestion.loader.FileLoader.load", fake_file_load)

    loader = DirectoryLoader(str(directory))
    docs = loader.load()

    assert len(docs) == 2
    assert docs[0]["metadata"]["source"] == "a.txt"
    assert docs[1]["metadata"]["source"] == "b.txt"
