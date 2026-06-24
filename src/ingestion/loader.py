from markitdown import MarkItDown
from pathlib import Path
from datetime import datetime
from typing import Optional
from abc import ABC, abstractmethod

SUPPORT_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx",
    ".html", ".htm", ".txt", ".md",
    ".jpg", ".jpeg", ".png"
}
# objective: init once at module level
mid = MarkItDown(
    cu_endpoint="<content_understanding_endpoint"
)
class BaseLoader(ABC):
    """
    All loader must implement load()
    """

    @abstractmethod
    def load(self) -> Optional[dict]:
        pass

    def _build_metadata(
        self,
        source:str,
        file_type:str,
        file_path:str
    ) -> dict:
        """Shared metadata builder for all subclasses"""
        return {
            "source":source,
            "file_path":file_path,
            "file_type":file_type,
            "loaded_at":datetime.today().isoformat()
        }

class FileLoader(BaseLoader):
    """
    Drop and Drag files directly to platform
    """
    def __init__(
        self,
        file_path:str
    ):
        self.file_path = Path(file_path)
    def load(self) -> Optional[dict]:
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        if self.file_path.suffix.lower() not in SUPPORT_EXTENSIONS:
            raise ValueError(f"Unsupported type: {self.file_path.suffix.lower()}") 

        try:
            result = mid.convert(str(self.file_path))
            text = result.text_content.strip()

            if not text:
                return None

            with open(f"md_store/{self.file_path.stem}.md", "w", encoding="utf-8") as f:
                print(f"Writing: {self.file_path.stem} as markdown format")
                f.write(result.markdown)

            return {
                "text":text,
                "metadata": self._build_metadata(
                    source=self.file_path.name,
                    file_type=self.file_path.suffix.lower().lstrip("."),
                    file_path=str(self.file_path.resolve())
                )
            }

        except Exception as e:
            print(f"[FileLoader] Failed: {e}")
            return None

class DirectoryLoader(BaseLoader):
    """
    Drop and drag a directory_path input
    """
    def __init__(
        self, 
        dir_path:str
    ):
        self.dir_path = Path(dir_path)

    def load(self) -> list[dict]:
        if not self.dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {self.dir_path}")

        docs = []
        for file in sorted(self.dir_path.rglob("*")):
            if file.suffix.lower() in SUPPORT_EXTENSIONS:
                doc = FileLoader(str(file)).load()
                if doc:
                    docs.append(doc)

        print(f"[DirectoryLoader] Loaded {len(docs)} docs from {self.dir_path}")
        return docs

class URLLoader(BaseLoader):
    def __init__(
        self,
        url:str
    ):
        self.url = url
    def load(self) -> Optional[dict]:
        try:
            result = mid.convert(self.url)
            text = result.text_content.strip()

            if not text:
                return None

            return {
                "text":text,
                "metadata": self._build_metadata(
                    source=self.url,
                    file_type="url",
                    file_path=self.url
                )
            }
        except Exception as e:
            print(f"[URLLoader] Failed: {e}")
            return None