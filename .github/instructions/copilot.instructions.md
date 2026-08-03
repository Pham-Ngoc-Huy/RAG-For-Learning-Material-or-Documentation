# Context
Retrieval Argument Generator (RAG-based Q&A) platform: users upload documents, ask questions against them,
and the system surfaces relationships between documents. Multi-tenant — each user has an isolated knowledge
base behind login/registration, with zero data overlap or overwrite between accounts.

## Architecture
- Backend: Python (FastAPI/Flask), OOP with base classes and inheritance
  (e.g. `BaseRetriever` -> `QdrantRetriever`, `BaseGenerator` -> provider-specific implementations)
- Multi-tenancy: each user gets an isolated collection/namespace in the vector store, keyed by user_id.
  Enforce isolation at the data-access layer, not just in application logic — never construct a query
  that could cross collections.
- Auth: registration + login required before any retrieval/generation access. Passwords hashed,
  sessions never shared across tenants.
- C++ used only where this repo is shared with non-RAG (e.g. control-system) projects — keep C++
  conventions generic, not RAG-specific.

## Response requirements
- Every answer must cite the source chunk/document (id + page/section if available)
- If the question requires a calculation, show the equation (plain math notation or LaTeX) before the numeric result
- If retrieved context doesn't support an answer, say so explicitly — never fill gaps from general knowledge
- Structure every answer as: Objective → Process → Output (with example) → Confidence level → Tokens used

## Confidence & token reporting
- Confidence level: report as a percentage (0-100%), derived from retrieval similarity score
  (e.g. cosine similarity normalized to 0-100) combined with generator's self-reported certainty if available.
  Do not fabricate a percentage when no similarity score is available — state "confidence unavailable" instead.
- Token count: report as an integer, taken from the LLM provider's response `usage` field
  (prompt_tokens + completion_tokens), not estimated.
- Cost conversion: convert token count to VND using:
  1. token count -> USD cost, based on the active model's per-token pricing (input/output priced separately if applicable)
  2. USD -> VND, using a configurable exchange rate constant (`USD_TO_VND_RATE`) stored in config/env,
     not hardcoded inline — this rate must be updated periodically and never assumed current.
  - Report format: `Tokens used: 1234 (~$0.0056 USD / ~140,000 VNĐ)`

## Documentation
- Each project folder includes a docs/ directory in Markdown: one file per module covering purpose,
  inputs/outputs, and dependencies
- Update docs/ in the same PR as code changes — stale docs are treated as a bug

## Code comments (Python & C++)
Required on every public function/method:
- @brief
- @param
- @objective
- @update date
- @commented by

## Things to avoid
- Don't go out of scope — no speculative suggestions without evidence in the retrieved context
- Don't invent citations or attribute an answer to a document that wasn't retrieved
- Don't let one user's query touch another user's data/collection, even for debugging or testing
- Don't hardcode credentials, API keys, connection strings, or exchange rates — use environment variables/config
- Don't suggest global mutable state for session/user context — pass user_id explicitly through the call chain