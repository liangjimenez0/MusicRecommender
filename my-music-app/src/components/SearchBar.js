import React, { useState } from "react";
import "/Users/liangjimenez/2024/fall/ai/music-recommender/my-music-app/src/components/App.css";

const SearchBar = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);

  // Fetch matching songs from the `/search` endpoint
  const handleSearch = async (searchTerm) => {
    if (!searchTerm.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/search?query=${encodeURIComponent(searchTerm)}`
      );
      if (response.ok) {
        const data = await response.json();
        setSearchResults(data.songs || []);
      } else {
        console.error("Failed to fetch search results");
      }
    } catch (error) {
      console.error("Error occurred while fetching search results:", error);
    }
  };

  const handleInputChange = (e) => {
    setSearchTerm(e.target.value);
    handleSearch(e.target.value);
  };

  const handleSongClick = (song) => {
    setSearchTerm(song.track_name); // Set the input to the selected song
    setSearchResults([]); // Hide dropdown
    onSearch(song.track_name); // Pass the selected song to the parent component
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search for a song to get recommendations..."
        value={searchTerm}
        onChange={handleInputChange}
        className="form-control"
      />
      {searchResults.length > 0 && (
        <div className="dropdown">
          {searchResults.map((song, index) => (
            <div
              key={index}
              className="dropdown-item"
              onClick={() => handleSongClick(song)}
            >
              <span className="bold">{song.track_name}</span> by {song.artists}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchBar;
