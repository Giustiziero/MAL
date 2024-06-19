import React, { useState } from 'react';
import './App.css';
import { Grommet, Box, Spinner } from 'grommet';
import SearchBar from './components/SearchBarGrommet';
import ResultBox from './components/ResultBoxGrommet';
import axios from 'axios';

const theme = {
  global: {
    font: {
      family: 'Arial',
      size: '14px',
      height: '20px',
    },
  },
};

function App() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  
  const getRec = async (query) => {
    setLoading(true);
  
    // Get animes
    try {
      const response = await axios.get('http://127.0.0.1:5000/get_similar_animes', {
        params: {
          anime_name: query        
        },
      });
      setResults(response.data);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    // <div>
    //   <SearchBar onSearch={getRec} />
    //   {/* {loading && <Loader />} */}
    //   {results != null && <ResultBox recList={results} />}
    // </div>
  <Grommet theme={theme} full>
    <img style={{ top: 0, position: "absolute", zIndex: -1 }} src="/header_image.jpeg" />
    <Box overflow="auto" fill align="center" justify="center" pad="large" gap="medium">
      <Box width="large">
          <SearchBar onSearch={getRec} />
      </Box>
      {loading && <Spinner />}
      {results != null && <ResultBox recList={results} />}
    </Box>
  </Grommet>
  );
}

export default App;
