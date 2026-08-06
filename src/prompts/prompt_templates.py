from abc import ABC, abstractmethod
from pathlib import Path

SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent / "system_prompt.md"

class PromptTemplate(ABC):
    """Abstract base class for prompt template implementations.

    @brief Define a reusable prompt formatting contract.
    @objective Allow prompt builders to produce final prompt text from templates.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    @abstractmethod
    def build(self, **kwargs) -> str:
        """Format the prompt template with provided keyword arguments.

        @brief Build the final prompt text.
        @param kwargs: template variables such as 'query', 'retrieved_chunks', or other prompt fields.
        @return: formatted prompt string.
        """
        pass

class SimplePromptTemplate(PromptTemplate):
    """In-memory format string prompt template.

    @brief Build a prompt from a Python string template.
    @objective Support prompt rendering without external files.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    def __init__(self, template: str):
        """Initialize with a string template.

        @param template: prompt string with Python format placeholders.
        """
        self.template = template

    def build(self, **kwargs) -> str:
        """Format the template with provided context.

        @brief Build final prompt string.
        @param kwargs: 'query' (str), 'retrieved_chunks' (list of dicts with id, score, payload.text)
        @return: formatted prompt string
        """
        return self.template.format(**kwargs)

class RAGPromptTemplate(PromptTemplate):
    """RAG-specific prompt template that integrates retrieved chunks with similarity scores.

    @brief Build a prompt from system guidelines + retrieved context + user query.
    @objective Format vectordb output (chunks with scores) into a coherent LLM prompt.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    def __init__(self, system_prompt_file: str | Path = SYSTEM_PROMPT_PATH):
        """Initialize with a system prompt file.

        @param system_prompt_file: path to markdown system prompt
        """
        self.system_prompt_file = Path(system_prompt_file)

    def build(self, **kwargs) -> str:
        """Build a complete RAG prompt with context chunks and user query.

        @brief Integrate vectordb retrieval results into a cohesive prompt.
        @param kwargs: must contain 'query' (str) and 'retrieved_chunks' (list of dicts)
                      each chunk dict: {id: str, score: float, payload: {text: str, ...metadata}}
        @return: formatted RAG prompt string
        @update date 2026-08-07
        @commented by Huy Pham
        """
        query = kwargs.get("query", "")
        retrieved_chunks = kwargs.get("retrieved_chunks", [])

        system_prompt = self.system_prompt_file.read_text(encoding="utf-8")

        # Format retrieved chunks with metadata and scores
        context_sections = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            chunk_id = chunk.get("id", f"chunk_{i}")
            score = chunk.get("score", 0.0)
            payload = chunk.get("payload", {})
            text = payload.get("text", "")

            context_section = f"""[CHUNK {i}] (ID: {chunk_id}, Relevance: {score:.2%})
{text}
"""
            context_sections.append(context_section)

        context = "\n".join(context_sections) if context_sections else "[No relevant documents found]"

        # Build final prompt
        final_prompt = f"""{system_prompt}

---

## RETRIEVED CONTEXT

{context}

---

## USER QUESTION

{query}

---

## ANSWER
"""
        return final_prompt

class FilePromptTemplate(PromptTemplate):
    """Load and render a prompt from a markdown file.

    @brief Build a prompt from an external markdown source.
    @objective Keep system prompt text editable outside Python code.
    @update date 2026-08-07
    @commented by Huy Pham
    """

    def __init__(self, file_path: str | Path = SYSTEM_PROMPT_PATH):
        """Initialize the file-backed prompt template.

        @param file_path: path to the markdown prompt file.
        """
        self.file_path = Path(file_path)

    def build(self, **kwargs) -> str:
        """Read the markdown prompt file and format it.

        @param kwargs: template variables such as 'documents'.
        @return: formatted prompt text.
        """
        template = self.file_path.read_text(encoding="utf-8")
        documents = kwargs.get("documents", [])
        if documents:
            kwargs["documents"] = "\n".join(documents)

        return f"""
            [system guidelines]
            {template.format(**kwargs)}
            [user prompt - question]
            {documents if documents else "No documents provided."}
"""


def load_system_prompt() -> str:
    """Return the system prompt from the markdown file.

    @brief Load the system prompt text for the LLM.
    @objective Move prompt configuration into a markdown file for easy editing.
    @return: raw system prompt text.
    @update date 2026-08-07
    @commented by Huy Pham
    """
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
