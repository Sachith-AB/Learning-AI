// src/App.jsx
import { useState } from "react";
import { 
  Card, 
  Button, 
  TextInput, 
  Badge, 
  Spinner, 
  Alert,
  Select,
  Navbar
} from "flowbite-react";
import { 
  HiSearch, 
  HiLocationMarker, 
  HiStar, 
  HiTag,
  HiHeart,
  HiEye,
  HiSparkles
} from "react-icons/hi";

import useRecommendations from "./hooks/useRecommendations";

function App() {
  const [query, setQuery] = useState("");
  const [submittedQuery, setSubmittedQuery] = useState("");
  const [resultCount, setResultCount] = useState(5);
  const [minScore, setMinScore] = useState(0.0);

  const { data, loading, error, totalResults, message } = useRecommendations(
    submittedQuery, 
    resultCount, 
    minScore
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      setSubmittedQuery(query.trim());
    }
  };

  const getPopularityColor = (popularity) => {
    switch (popularity) {
      case "very_high": return "success";
      case "high": return "info";
      case "medium": return "warning";
      case "low": return "gray";
      default: return "gray";
    }
  };

  const getPopularityIcon = (popularity) => {
    switch (popularity) {
      case "very_high": return "🔥";
      case "high": return "⭐";
      case "medium": return "👍";
      case "low": return "📍";
      default: return "📍";
    }
  };

  const quickSearches = [
    "beautiful beaches",
    "historical sites", 
    "adventure hiking",
    "wildlife safari",
    "cultural temples",
    "tea plantations",
    "family vacation"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <Navbar fluid rounded className="bg-white shadow-lg mb-8">
        <Navbar.Brand>
          <span className="text-2xl font-bold text-green-600">🌴 Sri Lanka Explorer</span>
        </Navbar.Brand>
        <div className="flex items-center space-x-2">
          <Badge color="info" size="sm">
            AI-Powered Search
          </Badge>
        </div>
      </Navbar>

      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
            Discover Sri Lanka's Hidden Gems ✨
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Find your perfect destination with AI-powered recommendations
          </p>
        </div>

        {/* Search Section */}
        <Card className="mb-8 shadow-xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1">
                <TextInput
                  icon={HiSearch}
                  placeholder="Search for beaches, temples, adventure spots, wildlife..."
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  sizing="lg"
                  className="w-full"
                />
              </div>
              <Button 
                type="submit" 
                size="lg"
                gradientDuoTone="greenToBlue"
                disabled={loading || !query.trim()}
                className="min-w-[120px]"
              >
                {loading ? (
                  <>
                    <Spinner size="sm" className="mr-2" />
                    Searching...
                  </>
                ) : (
                  <>
                    <HiSearch className="mr-2 h-5 w-5" />
                    Explore
                  </>
                )}
              </Button>
            </div>

            {/* Advanced Options */}
            <div className="flex flex-col md:flex-row gap-4 pt-4 border-t border-gray-200">
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Results
                </label>
                <Select
                  value={resultCount}
                  onChange={(e) => setResultCount(parseInt(e.target.value))}
                >
                  <option value={3}>3 results</option>
                  <option value={5}>5 results</option>
                  <option value={10}>10 results</option>
                  <option value={15}>15 results</option>
                </Select>
              </div>
              <div className="flex-1">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Minimum Relevance Score
                </label>
                <Select
                  value={minScore}
                  onChange={(e) => setMinScore(parseFloat(e.target.value))}
                >
                  <option value={0.0}>Any relevance</option>
                  <option value={0.3}>30% relevance</option>
                  <option value={0.5}>50% relevance</option>
                  <option value={0.7}>70% relevance</option>
                </Select>
              </div>
            </div>
          </form>

          {/* Quick Search Suggestions */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <p className="text-sm font-medium text-gray-700 mb-3">Quick searches:</p>
            <div className="flex flex-wrap gap-2">
              {quickSearches.map((suggestion, idx) => (
                <Badge
                  key={idx}
                  color="light"
                  className="cursor-pointer hover:bg-blue-100 transition-colors"
                  onClick={() => {
                    setQuery(suggestion);
                    setSubmittedQuery(suggestion);
                  }}
                >
                  {suggestion}
                </Badge>
              ))}
            </div>
          </div>
        </Card>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="text-center">
              <Spinner size="xl" />
              <p className="mt-4 text-lg text-gray-600">
                Searching for amazing destinations...
              </p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Alert color="failure" className="mb-6">
            <span className="font-medium">Search Error:</span> {error}
          </Alert>
        )}

        {/* Search Results */}
        {!loading && data && data.length > 0 && (
          <div className="space-y-6">
            {/* Results Header */}
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-800">
                Search Results for "{submittedQuery}"
              </h2>
              <Badge color="info" size="lg">
                {totalResults || data.length} locations found
              </Badge>
            </div>

            {message && (
              <Alert color="info" className="mb-4">
                <HiSparkles className="mr-2" />
                {message}
              </Alert>
            )}

            {/* Results Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {data.map((place, idx) => (
                <Card 
                  key={idx} 
                  className="hover:shadow-xl transition-shadow duration-300 border-l-4 border-l-green-500"
                >
                  <div className="space-y-4">
                    {/* Header with rank and score */}
                    <div className="flex justify-between items-start">
                      <div className="flex items-center space-x-2">
                        <Badge color="success" size="sm">
                          #{place.rank || idx + 1}
                        </Badge>
                        {place.similarity_score && (
                          <Badge color="gray" size="sm">
                            {Math.round(place.similarity_score * 100)}% match
                          </Badge>
                        )}
                      </div>
                      <div className="flex items-center space-x-1">
                        <span className="text-lg">
                          {getPopularityIcon(place.popularity)}
                        </span>
                        <Badge 
                          color={getPopularityColor(place.popularity)} 
                          size="sm"
                        >
                          {place.popularity?.replace('_', ' ') || 'Unknown'}
                        </Badge>
                      </div>
                    </div>

                    {/* Location Name and Place */}
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 mb-2">
                        {place.name}
                      </h3>
                      <div className="flex items-center text-gray-600 mb-3">
                        <HiLocationMarker className="mr-1 h-4 w-4" />
                        <span className="text-sm">{place.location}</span>
                      </div>
                    </div>

                    {/* Description */}
                    {place.description_snippet && (
                      <p className="text-gray-700 text-sm leading-relaxed">
                        {place.description_snippet}
                      </p>
                    )}

                    {/* Tags */}
                    {place.tags && place.tags.length > 0 && (
                      <div>
                        <div className="flex items-center mb-2">
                          <HiTag className="mr-1 h-4 w-4 text-gray-500" />
                          <span className="text-sm font-medium text-gray-700">Tags:</span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {place.tags.slice(0, 4).map((tag, tagIdx) => (
                            <Badge key={tagIdx} color="light" size="xs">
                              {tag}
                            </Badge>
                          ))}
                          {place.tags.length > 4 && (
                            <Badge color="gray" size="xs">
                              +{place.tags.length - 4} more
                            </Badge>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Best For */}
                    {place.best_for && place.best_for.length > 0 && (
                      <div>
                        <div className="flex items-center mb-2">
                          <HiHeart className="mr-1 h-4 w-4 text-gray-500" />
                          <span className="text-sm font-medium text-gray-700">Best for:</span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {place.best_for.slice(0, 3).map((activity, actIdx) => (
                            <Badge key={actIdx} color="info" size="xs">
                              {activity}
                            </Badge>
                          ))}
                          {place.best_for.length > 3 && (
                            <Badge color="gray" size="xs">
                              +{place.best_for.length - 3} more
                            </Badge>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Action Button */}
                    <Button 
                      color="light" 
                      size="sm"
                      className="w-full mt-4"
                      onClick={() => {
                        // You can add functionality to view more details
                        alert(`More details about ${place.name} coming soon!`);
                      }}
                    >
                      <HiEye className="mr-2 h-4 w-4" />
                      View Details
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* No Results */}
        {!loading && submittedQuery && data && data.length === 0 && (
          <Card className="text-center py-12">
            <div className="space-y-4">
              <div className="text-6xl">🔍</div>
              <h3 className="text-xl font-bold text-gray-800">
                No locations found
              </h3>
              <p className="text-gray-600">
                Try different keywords like "beach", "temple", "hiking", or "wildlife"
              </p>
              <div className="pt-4">
                <Button 
                  color="light"
                  onClick={() => {
                    setQuery("");
                    setSubmittedQuery("");
                  }}
                >
                  Clear Search
                </Button>
              </div>
            </div>
          </Card>
        )}

        {/* Footer */}
        <div className="text-center mt-12 pt-8 border-t border-gray-200">
          <p className="text-gray-500">
            Powered by AI • Discover the beauty of Sri Lanka 🇱🇰
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;