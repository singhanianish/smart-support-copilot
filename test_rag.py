from rag.loader import (
    load_text_file,
    split_text
)

from rag.embedder import (
    generate_embeddings
)

from rag.vectorstore import (
    VectorStore
)

from rag.retriever import (
    retrieve_context
)


# Load manual
text = load_text_file(
    "data/uploaded_pdfs/manual.txt"
)

# Split into chunks
chunks = split_text(text)

print(f"Total Chunks: {len(chunks)}")


# Generate embeddings
embeddings = generate_embeddings(chunks)

print("Embeddings generated")


# Create vector store
dimension = len(embeddings[0])

vector_store = VectorStore(dimension)

vector_store.add_embeddings(
    embeddings,
    chunks
)

print("FAISS index created")


# Test retrieval
query = "Why is my Galaxy phone overheating?"

results = retrieve_context(
    query,
    vector_store
)

print("\nRetrieved Context:\n")

for i, result in enumerate(results):
    print(f"\nResult {i+1}:\n")
    print(result)