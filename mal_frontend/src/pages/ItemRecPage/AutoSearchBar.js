import React, { useState, useEffect } from 'react';
import { TextInput, Button } from 'grommet';
import { Search } from 'grommet-icons';
import axios from 'axios';
import '../../App.css';  // Ensure your CSS styles are imported

const AutocompleteSearchBar = ({ onSearch }) => {
  const [value, setValue] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [allSuggestions, setAllSuggestions] = useState([]);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/suggestions');
        setAllSuggestions(response.data);
        console.log('Fetched suggestions:', response.data);
      } catch (error) {
        console.error('Error fetching suggestions:', error);
      }
    };

    fetchSuggestions();
  }, []);

  useEffect(() => {
    if (value.trim() !== '') {
      const filteredSuggestions = allSuggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(filteredSuggestions);
    } else {
      setSuggestions([]);
    }
  }, [value, allSuggestions]);

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
