import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import Recommendations from "./components/Recommendations";
import "./App.css";

const App = () => {
  const [recommendations, setRecommendations] = useState([]);

  const handleSearch = async (song) => {
    // If the search query is empty, clear the recommendations
    if (!song) {
      setRecommendations([]);
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/recommend?song=${encodeURIComponent(song)}`
      );
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      setRecommendations([]);
    }
  };

  return (
    <div className="app">
      <SearchBar onSearch={handleSearch} />
      <Recommendations recommendations={recommendations} />
    </div>
  );
};

export default App;
