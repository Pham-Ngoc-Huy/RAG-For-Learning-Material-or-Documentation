from abc import ABC, abstractmethod
from typing import Optional
import re

# token/char per chunk
DEFAULT_CHUNK_SIZE = 512
# overlap between consecutive chunks
DEFAULT_CHUNK_OVERLAP = 50
class BaseChunker(ABC):
    def __init__(
        self, 
        chunk_size: int=DEFAULT_CHUNK_SIZE,
        chunk_overlap: int=DEFAULT_CHUNK_OVERLAP
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    @abstractmethod
    def chunk(
        self, 
        doc: dict
    ) -> list[dict]:
        """
        Input: one doc dict from loader
        Output: list of chunk dicts
        """
        pass

    def chunk_many(
        self, 
        docs: list[dict]
    ) -> list[dict]:
        """
        Convience - chunk a list of docs (files) [DirectoryLoader output]
        """
        all_chunks = []
        for doc in docs:
            all_chunks.extend(self.chunk(doc))
        return all_chunks

    def _build_chunk_metadata(
        self,
        base_metadata:dict,
        chunk_index:int,
        total_chunk:int
    ) -> dict:
        return {
            **base_metadata,
            "chunk_index": chunk_index,
            "total_chunk": total_chunk
        }
class FixedSizeChunker(BaseChunker):
    """Split on charater count with overlap. 
        Simple, no structure awareness.
    """
    def chunk(self, doc:dict) -> list[dict]:
        text = doc["text"]
        metadata = doc["metadata"]
        chunks = []

        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start: end].strip()
            if chunk_text:
                chunks.append(chunk_text)

            start += self.chunk_size - self.chunk_overlap

        return [
            {
                "text": c,
                "metadata": self._build_chunk_metadata(metadata, i, len(chunks))
            }
            for i, c in enumerate(chunks)
        ]
class RecursiveChunker(BaseChunker):
    """
    Try splitting on separators in order:
        - Paragraph
            - newline
                - sentence
                    - word
    Respects natural text boundaries
    """
    SEPARATORS = ["\n\n", "\n", ". ", " "]
    def _split(
        self,
        text:str,
        sep_index: int=0
    ) -> list[dict]:
        """Recursively split using the next separtor when chunks are too large"""

        # no more separators - return as-is
        if sep_index >= len(self.SEPARATORS):
            return text
        
        sep = self.SEPARATORS[sep_index]
        pieces = text.split(sep)
        result = []
        # using index-SEPARATORS to look through the text to split if not keep searching in next index
        for piece in pieces:
            if len(piece) <= self.chunk_size:
                result.append(piece)
            else:
                result.extend(self._split(piece, sep_index + 1))

        return [p.strip() for p in result if p.strip()]
    def _merge(
        self,
        pieces: list[str]
    ) -> list[str]:
        """
        Merge small pieces back up to chunk_size, with overlap
        """

        chunks = []
        current = ""

        for piece in pieces:
            if len(current) + len(piece) + 1 <= self.chunk_size:
                current = (current + " " + piece).strip()
            else:
                if current:
                    chunks.append(current)

                overlap_text = current[-self.chunk_overlap:] if current else ""
                current = (overlap_text + " " + piece).strip()
        if current:
            chunks.append(current)
        return chunks
    
    def chunk(
        self,
        doc:dict 
    )->list[dict]:
        raw_chunks = self._split(doc["text"])
        merged = self._merge(raw_chunks)

        return [
            {
                "text":c,
                "metadata": self._build_chunk_metadata(
                    doc["metadata"], i, len(merged)
                )
            }
            for i, c in enumerate(merged)
        ]

class MarkDownChunker(BaseChunker):
    """
    Split on markdown headers first (##, ###), then recursively
    inside each section. Best for .md docs with clear structure.
    """
    HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    def _split_by_headers(
        self,
        text: str
    ) -> list[tuple[str,str]]:
        matches = list(self.HEADER_PATTERN.finditer(text))
        sections = []

        if not matches:
            return [("", text)]

        if matches[0].start() > 0:
            preamble = text[:matches[0].start()].strip()
            if preamble:
                sections.append(("", preamble))

        for i, match in enumerate(matches):
            title = match.group(2).strip()
            body_start = match.end()
            body_end = matches[i+1].start() if i+1 < len(matches) else len(text)
            body = text[body_start:body_end].strip()

            sections.append((title, f"## {title}\n{body}"))  # keep header in chunk

        return sections

    def chunk(
        self,
        doc:dict
    ) -> list[dict]:
        sections = self._split_by_headers(doc["text"])
        chunks = []
        for section_title, section_text in sections:
            if len(section_text) < self.chunk_size:
                if section_text.strip():
                    chunks.append(section_text.strip())
            else:
                sub = RecursiveChunker(self.chunk_size, self.chunk_overlap)
                sub_chunks = sub._split(section_text)
                merged = sub._merge(sub_chunks)
                chunks.extend(merged)


        return [
            {
                "text":c,
                "metadata": self._build_chunk_metadata(
                    doc["metadata"], i, len(chunks)
                )
            }
            for i,c in enumerate(chunks)
        ]