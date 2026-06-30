from intelligence.retrieval import (
    retrieve_documents,
    get_repository_statistics
)

# ==================================================
# Retrieval Tool
# ==================================================

def retrieval_tool(query, n_results=10):
    """
    Retrieve relevant documents from ChromaDB.
    """

    return retrieve_documents(
        query,
        n_results
    )


# ==================================================
# Repository Statistics
# ==================================================

def repository_statistics():
    """
    Return repository statistics.
    """

    return get_repository_statistics()