print(f"[Step 1] Using Qdrant URL: {qdrant_url}")
print(f"         To inspect via browser: {qdrant_url}\n")

try:
    vector_store = QdrantVectorStore()
    try:
        vector_store.delete_collection(user_id="test_user")
        print("  (Cleaned up old collection)")
    except:
        pass
    
    collection_name = vector_store.create_collection(
        user_id="test_user",
        vector_size=384,  # SentenceTransformer default embedding size
    )
    print(f"✓ Vector store initialized: {collection_name}\n")
except Exception as exc:
    print(f"✗ Vector store failed: {exc}")
    print(
        "  Make sure Qdrant is running and QDRANT_ENDPOINT is set.\n"
    )
    exit(1)

# ============================================================================
# STEP 2: Ingest & Embed Documents
# ============================================================================
print("[Step 2] Loading and embedding documents...")

try:
    # Load document
    doc_path = "temp/VGU ATHF PS 1.pdf"
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"Document not found: {doc_path}")

    doc_result = FileLoader(doc_path).load()
    if doc_result is None or not doc_result.get("text"):
        raise ValueError("Document loader returned empty content")

    docs_text = doc_result.get("text", "")
    print(f"  → Loaded document ({len(docs_text)} chars)")

    # Chunk document (pass the full dict with text and metadata)
    chunks = MarkDownChunker().chunk(doc=doc_result)
    print(f"  → Created {len(chunks)} chunks")

    # Embed chunks
    embedder = SentenceTransformerEmbedder()
    chunks = embedder.embed_many(chunks)
    print(f"  → Embedded chunks (dimension: 384)\n")

except Exception as exc:
    print(f"✗ Document ingestion failed: {exc}\n")
    exit(1)

# ============================================================================
# STEP 3: Store Chunks in Vector DB
# ============================================================================
print("[Step 3] Storing chunks in vector database...")

try:
    vector_store.upsert(user_id="test_user", chunks=chunks)
    print(f"✓ Stored {len(chunks)} chunks in vector store\n")
except Exception as exc:
    print(f"✗ Upsert failed: {exc}\n")
    exit(1)

# ============================================================================
# STEP 4: Retrieve Documents for a Query
# ============================================================================
print("[Step 4] Setting up retriever and testing with a question...")

try:
    retriever = QdrantRetriever(vector_store=vector_store, embedder=embedder)

    # Simple test query
    query = "What is this document about?"
    print(f"  Query: '{query}'\n")

    # Retrieve top-k relevant chunks
    retrieved_chunks = retriever.retrieve(
        user_id="test_user",
        query=query,
        top_k=3,  # Get top 3 most relevant chunks
    )

    print(f"✓ Retrieved {len(retrieved_chunks)} relevant chunks:\n")
    for i, chunk in enumerate(retrieved_chunks, 1):
        score = chunk.get("score", 0.0)
        text_snippet = chunk.get("payload", {}).get("text", "")[:100]
        print(f"  [{i}] Relevance: {score:.2%}")
        print(f"      Preview: {text_snippet}...\n")

except Exception as exc:
    print(f"✗ Retrieval failed: {exc}\n")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# STEP 5: Generate Answer using LLM + Retrieved Context
# ============================================================================
print("[Step 5] Generating answer with LLM...")

try:
    # Build RAG prompt with retrieved context
    prompt_template = RAGPromptTemplate()
    formatted_prompt = prompt_template.build(
        query=query,
        retrieved_chunks=retrieved_chunks,
    )

    print("  Generated prompt (first 300 chars):")
    print(f"  {formatted_prompt[:300]}...\n")

    # Choose LLM provider based on available API keys
    has_deepseek = os.getenv("DEEPSEEK_API_KEY") is not None
    has_openai = os.getenv("OPENAI_API_KEY") is not None
    
    if has_deepseek:
        print("  → Using DeepSeek API (DEEPSEEK_API_KEY detected)")
        llm = DeepSeekClient()
    elif has_openai:
        print("  → Using OpenAI API (OPENAI_API_KEY detected)")
        llm = OpenAIClient()
    else:
        print("  → Using mock LLM (no API keys set)")
        llm = LocalLLMClient()

    messages = [
        {"role": "user", "content": formatted_prompt}
    ]

    # Generate response
    response = llm.generate(
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )

    print(f"\n✓ LLM Response:\n")
    print(f"  Model: {response.get('model')}")
    print(f"  Tokens used: {response.get('tokens_used')}")
    print(f"  Stop reason: {response.get('stop_reason')}\n")
    print(f"  Answer:\n")
    print(f"  {response.get('response')}\n")

    reasoning_details = response.get("reasoning_details")
    if reasoning_details is not None:
        print("  Reasoning details:\n")
        print(f"  {json.dumps(reasoning_details, indent=2) if not isinstance(reasoning_details, str) else reasoning_details}\n")

    # Preserve reasoning details for a second verification call if supported
    if has_deepseek and reasoning_details is not None:
        print("  → Preserving reasoning_details and asking a follow-up verification question")
        messages.append(
            {
                "role": "assistant",
                "content": response.get("response"),
                "reasoning_details": reasoning_details,
            }
        )
        messages.append(
            {
                "role": "user",
                "content": "Are you sure? Think carefully.",
            }
        )

        followup = llm.generate(
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )

        print(f"\n✓ Follow-up LLM Response:\n")
        print(f"  Model: {followup.get('model')}")
        print(f"  Tokens used: {followup.get('tokens_used')}")
        print(f"  Stop reason: {followup.get('stop_reason')}\n")
        print(f"  Answer:\n")
        print(f"  {followup.get('response')}\n")
        followup_reasoning_details = followup.get("reasoning_details")
        if followup_reasoning_details is not None:
            print("  Follow-up reasoning details:\n")
            print(f"  {json.dumps(followup_reasoning_details, indent=2) if not isinstance(followup_reasoning_details, str) else followup_reasoning_details}\n")

except Exception as exc:
    print(f"✗ Generation failed: {exc}\n")
    import traceback
    traceback.print_exc()
    exit(1)

print()
print("=" * 70)
print("✓ FULL RAG PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 70)
