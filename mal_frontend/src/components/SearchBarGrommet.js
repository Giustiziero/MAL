import React, { useState } from 'react';
import { Box, TextInput, Button } from 'grommet';
import { Search } from 'grommet-icons';
import '../App.css';

const SearchBar = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = () => {
    if (onSearch) {
      onSearch(query);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="search-box">
      <TextInput
        plain
        placeholder="Anime name..."
        value={query}
        onChange={handleInputChange}
        onKeyDown={handleKeyPress}
        className="search-input"
      />
      <Button
        icon={<Search />}
        onClick={handleSearch}
        label="Recommend"
        primary
        className="search-button"
      />
    </div>
  );
};

export default SearchBar;
