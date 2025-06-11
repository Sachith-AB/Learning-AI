from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import chromadb
from chromadb.utils import embedding_functions
import logging
from typing import Optional, List, Dict, Any
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sri Lanka Location Recommender API", version="1.0.0")

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Added React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for ChromaDB
chroma_client = None
collection = None

def initialize_chromadb():
    """Initialize ChromaDB connection with error handling"""
    global chroma_client, collection
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        
        # Check if collection exists
        try:
            collection = chroma_client.get_collection(
                name="sri_lanka_locations",
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2")
            )
            logger.info("✅ ChromaDB collection loaded successfully")
        except ValueError:
            logger.error("❌ ChromaDB collection 'sri_lanka_locations' not found. Please run setup_chromadb.py first.")
            collection = None
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize ChromaDB: {str(e)}")
        chroma_client = None
        collection = None

# Initialize ChromaDB on startup
@app.on_event("startup")
async def startup_event():
    initialize_chromadb()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Sri Lanka Location Recommender API", "status": "running"}

@app.get("/api/health")
async def health_check():
    """Check if ChromaDB is properly initialized"""
    if collection is None:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "message": "ChromaDB not initialized. Please run setup_chromadb.py first."}
        )
    return {"status": "healthy", "collection_initialized": True}

@app.get("/api/recommend")
async def recommend_locations(
    query: str = Query(..., min_length=1, description="Search query for locations"),
    n: int = Query(5, ge=1, le=20, description="Number of results to return"),
    min_score: float = Query(0.0, ge=0.0, le=1.0, description="Minimum similarity score threshold")
):
    """
    Recommend locations based on semantic search
    
    Args:
        query: Search query (e.g., "beach vacation", "historical sites", "adventure")
        n: Number of results to return (1-20)
        min_score: Minimum similarity score (0.0-1.0)
    
    Returns:
        JSON response with recommended locations
    """
    if collection is None:
        raise HTTPException(
            status_code=503, 
            detail="ChromaDB collection not initialized. Please run setup_chromadb.py first."
        )
    
    try:
        logger.info(f"🔍 Searching for: '{query}' (n={n}, min_score={min_score})")
        
        # Perform semantic search
        results = collection.query(
            query_texts=[query],
            n_results=n,
            include=["metadatas", "distances", "documents"]
        )
        
        if not results["metadatas"] or not results["metadatas"][0]:
            return {
                "query": query,
                "results": [],
                "message": "No locations found matching your query"
            }
        
        # Process results with similarity scores
        processed_results = []
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        documents = results.get("documents", [[]])[0]
        
        for i, (metadata, distance, document) in enumerate(zip(metadatas, distances, documents)):
            # Convert distance to similarity score (lower distance = higher similarity)
            similarity_score = max(0.0, 1.0 - distance)
            
            # Apply minimum score filter
            if similarity_score >= min_score:
                result_item = {
                    "rank": i + 1,
                    "similarity_score": round(similarity_score, 3),
                    "name": metadata.get("name", "Unknown"),
                    "location": metadata.get("location", "Unknown"),
                    "tags": metadata.get("tags", "").split(", ") if metadata.get("tags") else [],
                    "best_for": metadata.get("best_for", "").split(", ") if metadata.get("best_for") else [],
                    "popularity": metadata.get("popularity", "Unknown"),
                    "description_snippet": document[:200] + "..." if len(document) > 200 else document
                }
                processed_results.append(result_item)
        
        logger.info(f"✅ Found {len(processed_results)} locations matching query")
        
        return {
            "query": query,
            "total_results": len(processed_results),
            "results": processed_results,
            "message": f"Found {len(processed_results)} locations matching '{query}'"
        }
        
    except Exception as e:
        logger.error(f"❌ Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/api/search-by-tag")
async def search_by_tag(
    tag: str = Query(..., description="Tag to search for (e.g., 'beach', 'historical')"),
    n: int = Query(10, ge=1, le=50, description="Number of results to return")
):
    """
    Search locations by specific tags
    """
    if collection is None:
        raise HTTPException(
            status_code=503, 
            detail="ChromaDB collection not initialized."
        )
    
    try:
        # Use tag-based semantic search
        tag_query = f"places for {tag} activities {tag} locations"
        
        results = collection.query(
            query_texts=[tag_query],
            n_results=n,
            include=["metadatas", "distances"]
        )
        
        if not results["metadatas"] or not results["metadatas"][0]:
            return {
                "tag": tag,
                "results": [],
                "message": f"No locations found with tag '{tag}'"
            }
        
        # Filter results that actually contain the tag
        filtered_results = []
        for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
            tags = metadata.get("tags", "").lower()
            best_for = metadata.get("best_for", "").lower()
            
            if tag.lower() in tags or tag.lower() in best_for:
                similarity_score = max(0.0, 1.0 - distance)
                filtered_results.append({
                    "name": metadata.get("name"),
                    "location": metadata.get("location"),
                    "tags": metadata.get("tags", "").split(", "),
                    "best_for": metadata.get("best_for", "").split(", "),
                    "popularity": metadata.get("popularity"),
                    "similarity_score": round(similarity_score, 3)
                })
        
        return {
            "tag": tag,
            "total_results": len(filtered_results),
            "results": filtered_results
        }
        
    except Exception as e:
        logger.error(f"❌ Tag search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Tag search failed: {str(e)}")

@app.get("/api/locations/all")
async def get_all_locations():
    """Get all locations in the database"""
    if collection is None:
        raise HTTPException(
            status_code=503, 
            detail="ChromaDB collection not initialized."
        )
    
    try:
        # Get all items from collection
        results = collection.get(include=["metadatas"])
        
        if not results["metadatas"]:
            return {"total": 0, "locations": []}
        
        locations = []
        for metadata in results["metadatas"]:
            locations.append({
                "name": metadata.get("name"),
                "location": metadata.get("location"),
                "tags": metadata.get("tags", "").split(", ") if metadata.get("tags") else [],
                "best_for": metadata.get("best_for", "").split(", ") if metadata.get("best_for") else [],
                "popularity": metadata.get("popularity")
            })
        
        return {
            "total": len(locations),
            "locations": locations
        }
        
    except Exception as e:
        logger.error(f"❌ Get all locations error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve locations: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)