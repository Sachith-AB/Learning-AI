// src/hooks/useRecommendations.js
import { useEffect, useState } from "react";

export default function useRecommendations(query, n = 5) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!query) return;

        setLoading(true);
        fetch(`http://localhost:8000/api/recommend?query=${encodeURIComponent(query)}&n=${n}`)
        .then((res) => {
            if (!res.ok) throw new Error("Failed to fetch");
            return res.json();
        })
        .then((data) => {
            setData(data.results || []);
            setLoading(false);
        })
        .catch((err) => {
            setError(err.message);
            setLoading(false);
        });
    }, [query, n]);

    return { data, loading, error };
}
