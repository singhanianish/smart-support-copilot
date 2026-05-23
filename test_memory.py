from memory.chat_memory import (
    ChatMemory
)

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


# Setup memory
memory = ChatMemory()


# Load documents
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


# First query
query1 = "Why is my Galaxy phone overheating?"

memory.add_message(
    "user",
    query1
)

query_type1 = classify_query(query1)

context1 = retrieve_context(
    query1,
    vector_store
)

response1 = generate_response(
    query1,
    query_type1,
    context1,
    memory.get_formatted_history()
)

memory.add_message(
    "assistant",
    response1
)

print("\nFIRST RESPONSE:\n")
print(response1)


# Follow-up query
query2 = "What if this keeps happening?"

memory.add_message(
    "user",
    query2
)

query_type2 = classify_query(query2)

context2 = retrieve_context(
    query2,
    vector_store
)

response2 = generate_response(
    query2,
    query_type2,
    context2,
    memory.get_formatted_history()
)

print("\nFOLLOW-UP RESPONSE:\n")
print(response2)