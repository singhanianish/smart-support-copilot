import streamlit as st
import tempfile
import os

from memory.chat_memory import ChatMemory

from rag.loader import (
    load_pdf,
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


# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Smart Support Copilot",
    layout="wide"
)

st.title("📱 Smart Support Copilot")

st.markdown(
    """
    AI-powered support assistant using:
    - RAG
    - Query Classification
    - Dynamic Routing
    - Conversational Memory
    """
)


# -----------------------------
# SESSION STATE
# -----------------------------

if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()

if "vector_store" not in st.session_state:

    from rag.loader import (
        load_text_file
    )

    sample_text = load_text_file(
        "data/uploaded_pdfs/manual.txt"
    )

    chunks = split_text(sample_text)

    embeddings = generate_embeddings(chunks)

    dimension = len(embeddings[0])

    vector_store = VectorStore(dimension)

    vector_store.add_embeddings(
        embeddings,
        chunks
    )

    st.session_state.vector_store = (
        vector_store
    )


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Upload Support Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

st.sidebar.markdown("### Supported Query Types")
st.sidebar.markdown("""
- Troubleshooting
- Product Comparison
- General Knowledge
""")


# -----------------------------
# PROCESS PDF
# -----------------------------

if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:

        tmp_file.write(uploaded_file.read())

        temp_path = tmp_file.name

    text = load_pdf(temp_path)

    chunks = split_text(text)

    embeddings = generate_embeddings(chunks)

    dimension = len(embeddings[0])

    vector_store = VectorStore(dimension)

    vector_store.add_embeddings(
        embeddings,
        chunks
    )

    st.session_state.vector_store = (
        vector_store
    )

    st.sidebar.success(
        "Document processed successfully!"
    )


# -----------------------------
# DISPLAY CHAT HISTORY
# -----------------------------

for message in (
    st.session_state.memory.get_history()
):

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------
# CHAT INPUT
# -----------------------------

query = st.chat_input(
    "Ask your support question..."
)


# -----------------------------
# HANDLE QUERY
# -----------------------------

if query:

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.memory.add_message(
        "user",
        query
    )

    # Ensure documents uploaded
    if st.session_state.vector_store is None:

        response = (
            "Please upload a PDF document first."
        )

    else:

        with st.spinner("Generating response..."):

            # Query classification
            query_type = classify_query(query)
            st.info(
                f"Detected Query Type: {query_type}"
            )

            # Retrieve context
            context = retrieve_context(
                query=query,
                vector_store=(
                    st.session_state.vector_store
                ),
                chat_history=(
                    st.session_state.memory
                    .get_recent_history()
                )
            )

            # Generate response
            response = generate_response(
                query=query,
                query_type=query_type,
                context=context,
                chat_history=(
                    st.session_state.memory
                    .get_recent_history()
                )
            )

            # Generate response
            response = generate_response(
                query=query,
                query_type=query_type,
                context=context,
                chat_history=(
                    st.session_state.memory
                    .get_recent_history()
                )
            )

    # Store assistant response
    st.session_state.memory.add_message(
        "assistant",
        response
    )

    # Display assistant response
    with st.chat_message("assistant"):

        st.markdown(response)