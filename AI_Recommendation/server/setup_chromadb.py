import json
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import os
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_locations() -> List[Dict[str, Any]]:
    """Load locations from JSON file with error handling"""
    try:
        if not os.path.exists("sri_lanka_locations.json"):
            logger.error("❌ sri_lanka_locations.json not found!")
            logger.error("Please create sri_lanka_locations.json file with your location data.")
            raise FileNotFoundError("sri_lanka_locations.json file is required")
            
        with open("sri_lanka_locations.json", "r", encoding='utf-8') as f:
            locations = json.load(f)
            
        logger.info(f"✅ Loaded {len(locations)} locations from your JSON file")
        return locations
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON format in sri_lanka_locations.json: {str(e)}")
        raise
    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"❌ Error loading locations: {str(e)}")
        raise

# Removed sample data creation function - data should come from your JSON file

def validate_location_data(locations: List[Dict[str, Any]]) -> bool:
    """Validate location data structure"""
    required_fields = ["id", "name", "location", "description", "tags", "best_for", "popularity"]
    
    for i, loc in enumerate(locations):
        for field in required_fields:
            if field not in loc:
                logger.error(f"❌ Location {i} missing required field: {field}")
                return False
                
        # Validate data types
        if not isinstance(loc["tags"], list) or not isinstance(loc["best_for"], list):
            logger.error(f"❌ Location {i} has invalid data types for tags or best_for")
            return False
    
    logger.info("✅ Location data validation passed")
    return True

def create_enhanced_descriptions(locations: List[Dict[str, Any]]) -> List[str]:
    """Create enhanced descriptions for better semantic search"""
    descriptions = []
    
    for loc in locations:
        # Create rich description combining all available information
        enhanced_desc = f"""
        {loc['name']} in {loc['location']}: {loc['description']}
        
        This location is perfect for: {', '.join(loc['best_for'])}.
        Popular activities and features: {', '.join(loc['tags'])}.
        Popularity level: {loc['popularity']}.
        
        Keywords: {loc['name']}, {loc['location']}, {', '.join(loc['tags'])}, {', '.join(loc['best_for'])}
        """.strip()
        
        descriptions.append(enhanced_desc)
    
    return descriptions

def create_chroma_collection(locations: List[Dict[str, Any]]) -> None:
    """Create ChromaDB collection with enhanced error handling"""
    try:
        # Validate input data
        if not validate_location_data(locations):
            raise ValueError("Location data validation failed")
        
        logger.info("🚀 Starting ChromaDB setup...")
        
        # Initialize embedding model
        logger.info("📊 Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Create enhanced descriptions for better search
        logger.info("📝 Creating enhanced descriptions...")
        descriptions = create_enhanced_descriptions(locations)
        
        # Generate embeddings
        logger.info("🔮 Generating embeddings...")
        embeddings = model.encode(descriptions, show_progress_bar=True).tolist()
        
        # Prepare metadata
        logger.info("📋 Preparing metadata...")
        metadatas = [{
            "name": loc["name"],
            "location": loc["location"],
            "tags": ", ".join(loc["tags"]),
            "best_for": ", ".join(loc["best_for"]),
            "popularity": loc["popularity"],
            "description": loc["description"]  # Store original description
        } for loc in locations]
        
        ids = [loc["id"] for loc in locations]
        
        # Create ChromaDB client and collection
        logger.info("🗄️ Setting up ChromaDB...")
        client = chromadb.PersistentClient(path="./chroma_db")
        
        # Delete existing collection if it exists
        try:
            # Check if collection exists by trying to get it
            existing_collections = [col.name for col in client.list_collections()]
            if "sri_lanka_locations" in existing_collections:
                client.delete_collection("sri_lanka_locations")
                logger.info("🗑️ Deleted existing collection")
            else:
                logger.info("📂 No existing collection found - creating new one")
        except Exception as e:
            logger.info(f"📂 No existing collection found - creating new one ({str(e)})")
        
        # Create new collection
        collection = client.create_collection(
            name="sri_lanka_locations",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2"),
            metadata={"description": "Sri Lanka tourist locations with semantic search capabilities"}
        )
        
        # Add data to ChromaDB in batches for better performance
        logger.info("💾 Adding data to ChromaDB...")
        batch_size = 100
        
        for i in range(0, len(locations), batch_size):
            end_idx = min(i + batch_size, len(locations))
            
            collection.add(
                ids=ids[i:end_idx],
                embeddings=embeddings[i:end_idx],
                metadatas=metadatas[i:end_idx],
                documents=descriptions[i:end_idx]
            )
            
            logger.info(f"📦 Added batch {i//batch_size + 1} ({end_idx - i} items)")
        
        # Verify the collection
        count = collection.count()
        logger.info(f"✅ ChromaDB collection created successfully with {count} locations!")
        
        # Test the collection with a sample query
        logger.info("🔍 Testing collection with sample query...")
        test_results = collection.query(
            query_texts=["beautiful beach for swimming"],
            n_results=3,
            include=["metadatas", "distances"]
        )
        
        if test_results["metadatas"] and test_results["metadatas"][0]:
            logger.info("✅ Sample query successful - collection is working properly!")
            for i, metadata in enumerate(test_results["metadatas"][0]):
                distance = test_results["distances"][0][i]
                logger.info(f"  - {metadata['name']} (similarity: {1-distance:.3f})")
        else:
            logger.warning("⚠️ Sample query returned no results")
            
    except Exception as e:
        logger.error(f"❌ Error creating ChromaDB collection: {str(e)}")
        raise

def main():
    """Main function to set up ChromaDB"""
    try:
        logger.info("🌴 Sri Lanka Location Recommender - Database Setup")
        logger.info("=" * 50)
        
        # Load location data
        locations = load_locations()
        
        # Create ChromaDB collection
        create_chroma_collection(locations)
        
        logger.info("=" * 50)
        logger.info("🎉 Setup completed successfully!")
        logger.info("💡 You can now run the FastAPI server with: python main.py")
        logger.info("🔍 Test the API at: http://localhost:8000/docs")
        
    except Exception as e:
        logger.error(f"❌ Setup failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()