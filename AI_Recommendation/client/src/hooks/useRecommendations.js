// src/hooks/useRecommendations.js
import { useEffect, useState, useCallback } from "react";

export default function useRecommendations(query, n = 5, minScore = 0.0) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [totalResults, setTotalResults] = useState(0);
    const [message, setMessage] = useState("");

    // Memoize the fetch function to prevent unnecessary re-renders
    const fetchRecommendations = useCallback(async (searchQuery, resultCount, minimumScore) => {
        if (!searchQuery || searchQuery.trim() === "") return;

        setLoading(true);
        setError(null);
        setData([]);
        setMessage("");

        try {
            const params = new URLSearchParams({
                query: searchQuery.trim(),
                n: resultCount.toString(),
                min_score: minimumScore.toString()
            });

            const response = await fetch(`http://localhost:8000/api/recommend?${params}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                // Handle different HTTP status codes
                if (response.status === 503) {
                    throw new Error("Search service is temporarily unavailable. Please try again later.");
                } else if (response.status === 500) {
                    throw new Error("Internal server error. Please check your search query and try again.");
                } else {
                    throw new Error(`Search failed with status ${response.status}`);
                }
            }

            const result = await response.json();
            
            // Handle the improved API response structure
            if (result.results && Array.isArray(result.results)) {
                setData(result.results);
                setTotalResults(result.total_results || result.results.length);
                setMessage(result.message || "");
            } else {
                // Fallback for old API structure
                setData(result.results || []);
                setTotalResults(result.results?.length || 0);
            }

        } catch (err) {
            console.error("Search error:", err);
            setError(err.message || "An unexpected error occurred while searching.");
            setData([]);
            setTotalResults(0);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (query && query.trim()) {
            fetchRecommendations(query, n, minScore);
        } else {
            // Reset state when query is empty
            setData([]);
            setError(null);
            setTotalResults(0);
            setMessage("");
        }
    }, [query, n, minScore, fetchRecommendations]);

    // Return additional utility functions
    const refetch = useCallback(() => {
        if (query && query.trim()) {
            fetchRecommendations(query, n, minScore);
        }
    }, [query, n, minScore, fetchRecommendations]);

    const clearResults = useCallback(() => {
        setData([]);
        setError(null);
        setTotalResults(0);
        setMessage("");
    }, []);

    return { 
        data, 
        loading, 
        error, 
        totalResults,
        message,
        refetch,
        clearResults
    };
}

// Additional hook for tag-based search
export function useTagSearch(tag, n = 10) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!tag) return;

        setLoading(true);
        setError(null);

        const fetchTagResults = async () => {
            try {
                const params = new URLSearchParams({
                    tag: tag,
                    n: n.toString()
                });

                const response = await fetch(`http://localhost:8000/api/search-by-tag?${params}`);
                
                if (!response.ok) {
                    throw new Error(`Tag search failed with status ${response.status}`);
                }

                const result = await response.json();
                setData(result.results || []);
            } catch (err) {
                console.error("Tag search error:", err);
                setError(err.message || "Tag search failed");
                setData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchTagResults();
    }, [tag, n]);

    return { data, loading, error };
}

// Hook to get all locations
export function useAllLocations() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        setError(null);

        const fetchAllLocations = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/locations/all');
                
                if (!response.ok) {
                    throw new Error(`Failed to fetch locations with status ${response.status}`);
                }

                const result = await response.json();
                setData(result.locations || []);
            } catch (err) {
                console.error("Fetch all locations error:", err);
                setError(err.message || "Failed to fetch locations");
                setData([]);
            } finally {
                setLoading(false);
            }
        };

        fetchAllLocations();
    }, []);

    return { data, loading, error };
}