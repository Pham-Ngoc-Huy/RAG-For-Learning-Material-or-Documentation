# Loader:

Load input `file/directory/url` and transform into `.md` file

## 1. File Extension Supporting:

File can read in this `loader.py` must have this suffix extension:

- pdf
- docx
- pptx
- xlsx
- html
- htn
- txt
- md
- jpg
- jpeg
- png

## 2. Loader

> **Result return:** The result of the `loader.py` will be a shared metadata builder which will has format:

```json
"source":source,
"file_path":file_path,
"file_type":file_type,
"loaded_at":datetime.today().isoformat()
```

### 2.1. File Loader (Subclass)

---

This function will handle input as `file` and return it as output format as `.md` file

**Usage:**

```python
from src.ingestion import FileLoader

doc = FileLoader(`file_path`).load()
# where file_path will be the `path` to file has suffix as the list `file extension supporting` above
```

### 2.2. Directory Loader (Subclass)

---

This function will handle input as `directory` which is it will turn all files in the `destination_path` into `.md` if it match the `file-extension-supporting`

**Usage**

```python
from src.ingestion import DirectoryLoader

docs = DirectoryLoader(`directory_path`).load()
# where file_path will be the `path` to directory where files has suffix as the list `file extension supporting` above
```

### 2.3. URL Loader (Subclass)

---

This function will handle input as `URL` and the action will crawl the `HTML` into `.md`

**Usage**

```python
from src.ingestion import URLLoader

page = URLLoader("https://example.com").load()
```

## 3. Functionality support in RAG

This ingestion module is designed to product a unified document loading interface for `RAG`

1. Unified Document Format
2. Markdown Normalization
3. Metadata Tracking
4. Multi-Source Ingestion
5. Chunking Compatibility
6. Embedding Pipeline Integration
7. Vector Database Integration (`Qdrant` supported)
8. Source Citation Support

## 4. References

[1] https://github.com/microsoft/markitdown
