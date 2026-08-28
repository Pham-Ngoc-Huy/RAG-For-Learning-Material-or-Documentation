# Prompt Templates

This module provides reusable prompt formatting utilities for the RAG pipeline.

## Purpose

- Render LLM prompts from either in-memory string templates or an external markdown file.
- Keep system prompt text editable outside of Python source code.

## Files

- `src/prompts/prompt_templates.py`: prompt template classes and loader helper.
- `src/prompts/system_prompt.md`: editable system prompt source.

## Inputs

- `template` string for `SimplePromptTemplate`
- `file_path` for `FilePromptTemplate`
- `documents` list for prompt rendering

## Outputs

- formatted prompt string ready to be passed to the LLM client

## Notes

- `SYSTEM_PROMPT_PATH` points to `src/prompts/system_prompt.md`.
- `load_system_prompt()` reads the markdown file and returns its text.
