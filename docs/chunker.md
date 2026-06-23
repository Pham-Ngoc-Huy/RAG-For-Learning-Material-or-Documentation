# Chunker
## 1. Why Chunk ?
>Your loaded doc might be 50 pages. You can't pass all of it to the LLM (context limit) or embed it as one vector (too noisy - one vector can't represent 50 pages meaningfully). So this need to split into focused pieces.

## 2. Strategies:
We have 3 types of strategies in `chunking`  
**For example**:

```python
input_text = """
The sky is bule.

Stars are far away.
The moon reflects light.

Space is vast and contains many galaxies and nebulae and black holes and supernovae
"""

```
### 2.1. Strategy 1 - [Fixed Size]
---
Just cuts at every N characters, slides a window with overlap. Ignores all structure
```
chunk_size=50, overlap=10

text:  "The sky is blue.\n\nStars are far away.\nThe moon..."
        |←────── 50 ──────→|
                      |←── 50 ──→|
                                    overlap=10 ↑
```
```
chunk 0: "The sky is blue.\n\nStars are far away.\nThe mo"
chunk 1: "The mo on reflects light.\n\nSpace is vast and"
chunk 2: "st and contains many galaxies and nebulae..."
```

**Problem** - `"The mo" and "on reflects" got split mid-word. It doesn't care  
**Use when** - you just want something working fast , doc has no structure

### 2.2. Strategy 2 - [Recursive]
---
Tries separators **in order** - stops as soon as chunks are small enough
```
Priority:  "\n\n"  →  "\n"  →  ". "  →  " "
```  
**Step 1:** try split on `\n\n` (paragraph breaks):
```
piece A: "The sky is blue."                          ✅ fits
piece B: "Stars are far away.\nThe moon reflects."   ✅ fits  
piece C: "Space is vast and contains many galaxies   ❌ too big
          and nebulae and black holes and supernovae."
```
**Step 2:** piece C is too big → go deeper, try `\n`:
```
piece C has no \n → try ". "
"Space is vast and contains many galaxies"    ✅ fits
"and nebulae and black holes and supernovae"  ✅ fits
```
Then merge small pieces back up to fill chunk_size:
```
chunk 0: "The sky is blue. Stars are far away."
chunk 1: "The moon reflects light."
chunk 2: "Space is vast and contains many galaxies"
chunk 3: "and nebulae and black holes and supernovae"
```
**Use when** - plain prose, no markdown headers.

### Strategy 3 - [Markdown-Aware]
---
First splits on headers, then applies recursive inside each section.
Input `.md`:

```markdown
# Introduction
The sky is blue. Stars are far away.

# Space
Space is vast and contains many galaxies and nebulae 
and black holes and supernovae and quasars and pulsars 
and dark matter and cosmic dust and gravitational waves.

## Black Holes
Black holes warp spacetime significantly.
```
**Step 1**: split by headers:
```
section 1: "# Introduction"  -> "The sky is blue. Stars are far away."
section 2: "# Space"         -> "Space is vast and contains..." (too big)
section 3: "## Black Holes"  -> "Black holes warp spacetime."
```
**Step 2**: section 2 too big -> recursive kicks in inside it:
```
chunk 0: "## Introduction\nThe sky is blue. Stars are far away."
chunk 1: "## Space\nSpace is vast and contains many galaxies and nebulae"
chunk 2: "and black holes and supernovae and quasars and pulsars"
chunk 3: "and dark matter and cosmic dust and gravitational waves."
chunk 4: "## Black Holes\nBlack holes warp spacetime significantly."
```
>**Key difference**: the header `## Black Holes` stays attached to its content. When this chunk gets retrieved later, the LLM knows the context came from the "Black Holes" section.

**Note:**
>Without overlap, if a sentence spans a chunk boundary it gets cut and loses context. Overlap ensures boundary content appears in both adjacent chunks so nothing is lost.
