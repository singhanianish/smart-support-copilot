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

from logic.classifier import (
    classify_query
)

from logic.router import (
    generate_response
)


# Load data
text = load_text_file(
    "data/uploaded_pdfs/manual.txt"
)

chunks = split_text(text)

embeddings = generate_embeddings(chunks)

dimension = len(embeddings[0])

vector_store = VectorStore(dimension)

vector_store.add_embeddings(
    embeddings,
    chunks
)


# User query
query = "Why is my Galaxy phone overheating?"


# Classify
query_type = classify_query(query)

print(f"\nQuery Type: {query_type}")


# Retrieve
context = retrieve_context(
    query,
    vector_store
)

print("\nRetrieved Context Ready")


# Generate final response
response = generate_response(
    query,
    query_type,
    context
)

print("\nFinal Response:\n")

print(response)