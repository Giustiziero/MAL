import React, { useState } from 'react';
import { Box, Spinner, Image } from 'grommet';
import AutocompleteSearchBar from './AutoSearchBar';
import ResultBox from './ResultBoxGrommet';
import AnimeDetails from './AnimeDetails';  // Import the AnimeDetails component
import axios from 'axios';
import '../../App.css';

const ItemRec = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [animeDetails, setAnimeDetails] = useState(null);
  
  const getRec = async (query) => {
    setLoading(true);
  
    try {
      // const recResponse = await axios.get('https://malrec.azurewebsites.net/get_similar_animes', {
      const recResponse = await axios.get('http://127.0.0.1:5000/get_similar_animes', {
        params: { anime_name: query },
      });
      setResults(recResponse.data);
      
      const detailsResponse = await axios.get('http://127.0.0.1:5000/api/anime_details', {
        params: { anime_name: query },
        fields: ['main_picture', 'mean', 'genres', 'synopsis', 'title'] //image_url, score, genres, synopsis 
      });
      setAnimeDetails(detailsResponse.data);  
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box fill className="center-box" style={{ width: "auto" }}>
      <Box className='center-column'>
        <Box height="auto" width="auto" align='center' alignContent='center' alignSelf='center' overflow='hidden' pad='large' style={{ position: 'relative' }}>
          <Image
            fit="cover"
            src="/header_image.jpeg"
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              objectPosition: 'center',
            }}
          />
        </Box>
        <Box className='search-box-wrapper'>
          <AutocompleteSearchBar onSearch={getRec} />
        </Box>

        {loading && <Spinner />}
        
        {animeDetails && <AnimeDetails details={animeDetails} />}

        {results != null && (<ResultBox recList={results} />)}

      </Box>
    </Box>
  );
};

export default ItemRec;
