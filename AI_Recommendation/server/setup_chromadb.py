import json
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions

# --- Step 1: Load Dataset ---
def load_locations():
    with open("sri_lanka_locations.json", "r") as f:
        return json.load(f)

# --- Step 2: Initialize ChromaDB ---
def create_chroma_collection(locations):
    # Initialize embedding model (lightweight)
    model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dimensional vectors

    # Generate embeddings
    descriptions = [
        f"{loc['name']}: {loc['description']}. Tags: {', '.join(loc['tags'])}" 
        for loc in locations
    ]
    embeddings = model.encode(descriptions).tolist()

    # Prepare metadata
    metadatas = [{
        "name": loc["name"],
        "location": loc["location"],
        "tags": ", ".join(loc["tags"]),
        "best_for": ", ".join(loc["best_for"]),
        "popularity": loc["popularity"]
    } for loc in locations]

    ids = [loc["id"] for loc in locations]

    # Create ChromaDB collection (persistent)
    client = chromadb.PersistentClient(path="./chroma_db")  # Saves to disk
    collection = client.create_collection(
        name="sri_lanka_locations",
        embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
    )

    # Add data to ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=descriptions  # Optional: store full text
    )
    print("✅ ChromaDB collection created with", len(locations), "locations.")

# --- Run Script ---
if __name__ == "__main__":
    locations = load_locations()
    create_chroma_collection(locations)