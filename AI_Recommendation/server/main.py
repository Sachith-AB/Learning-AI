from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from chromadb.utils import embedding_functions

app = FastAPI()

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(
    name="sri_lanka_locations",
    embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
)

@app.get("/api/recommend")
async def recommend_locations(query: str, n: int = 5):
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n,
            include=["metadatas", "distances"]
        )
        return {"results": results["metadatas"][0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))