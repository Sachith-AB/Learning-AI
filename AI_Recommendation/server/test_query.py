import chromadb
from chromadb.utils import embedding_functions

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(
    name="sri_lanka_locations",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
)

# Semantic query
results = collection.query(query_texts=["beach"], n_results=5)

# Filter metadata (flatten the nested lists)
filtered = [
    doc for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    if "whales" in meta["tags"]
]

print("Filtered Results:\n", filtered)
