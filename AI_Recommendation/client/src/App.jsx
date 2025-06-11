// src/App.jsx
import { useState } from "react";
import useRecommendations from "./hooks/useRecommendations";

function App() {
  const [query, setQuery] = useState("");
  const [submittedQuery, setSubmittedQuery] = useState(null);

  const { data, loading, error } = useRecommendations(submittedQuery);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmittedQuery(query);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Sri Lanka Location Recommender 🌴</h1>
      <form onSubmit={handleSubmit}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. beach, hiking, whales"
          style={{ padding: "0.5rem", width: "300px" }}
        />
        <button type="submit" style={{ padding: "0.5rem", marginLeft: "0.5rem" }}>
          Search
        </button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {data.map((place, idx) => (
          <li key={idx}>
            <strong>{place.name}</strong> ({place.location}) — Tags: {place.tags}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
