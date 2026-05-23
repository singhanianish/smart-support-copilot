from rag.embedder import embedding_model


def retrieve_context(
    query,
    vector_store,
    chat_history="",
    top_k=3
):

    enhanced_query = (
        chat_history + "\n" + query
    )

    query_embedding = embedding_model.encode(
        enhanced_query
    )

    results = vector_store.search(
        query_embedding,
        top_k=top_k
    )

    return results