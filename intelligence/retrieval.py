import chromadb
from sentence_transformers import SentenceTransformer

# ==================================================
# Load Embedding Model
# ==================================================

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# ==================================================
# Connect to ChromaDB
# ==================================================

client = chromadb.PersistentClient(
    path="chroma_db_clean"
)

collection = client.get_collection(
    "sap_intelligence"
)

# ==================================================
# Retrieval Function
# ==================================================

def retrieve_documents(
    query,
    n_results=5
):
    """
    Retrieve the most relevant documents from ChromaDB.
    """

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    documents = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):

        documents.append(
            {
                "document": document,
                "metadata": metadata
            }
        )

    return documents

# ==================================================
# Knowledge Base Statistics
# ==================================================

def get_repository_statistics():
    """
    Return statistics about the entire ChromaDB repository.
    """

    data = collection.get()

    total_documents = len(data["ids"])

    sources = set()

    for metadata in data["metadatas"]:

        source = metadata.get("source", "Unknown")

        if source:
            sources.add(source)

    return {

        "documents": total_documents,

        "sources": sorted(list(sources))

    }

# ==================================================
# Standalone Test
# ==================================================

if __name__ == "__main__":

    query = input(
        "Enter question: "
    )

    results = retrieve_documents(
        query
    )

    print("\nTOP DOCUMENTS\n")

    for i, item in enumerate(
        results,
        start=1
    ):

        print("=" * 50)
        print(f"DOCUMENT {i}")
        print(item["metadata"].get("title", "Unknown"))
        print(item["document"][:1000])
        print()
        
    print("\nRepository Statistics")
    print(get_repository_statistics())