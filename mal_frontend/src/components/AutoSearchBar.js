import React, { useState, useEffect } from 'react';
import { Box, TextInput, Button } from 'grommet';
import { Search } from 'grommet-icons';
import axios from 'axios';
import '../App.css';  // Ensure your CSS styles are imported

const AutocompleteSearchBar = ({ onSearch }) => {
  const [value, setValue] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    if (value.trim() !== '') {
      const fetchSuggestions = async () => {
        try {
          const response = await axios.get('http://127.0.0.1:5000/api/suggestions', {
            params: { query: value },
          });
          setSuggestions(response.data);
        } catch (error) {
          console.error('Error fetching suggestions:', error);
        }
      };

      fetchSuggestions();
    } else {
      setSuggestions([]);
    }
  }, [value]);

  const handleInputChange = (event) => {
    setValue(event.target.value);
  };

  const handleSearch = () => {
    if (onSearch) {
      onSearch(value);
    }
  };

  return (
    <div className="search-box">
      <TextInput
        plain
        placeholder="Anime name..."
        value={value}
        onChange={handleInputChange}
        suggestions={suggestions}
        onSelect={(event) => setValue(event.suggestion)}
        className="search-input"
      />
      <Button
        plain
        icon={<Search />}
        onClick={handleSearch}
        label="Recommend"
        className="search-button"
      />
    </div>
  );
};

export default AutocompleteSearchBar;
