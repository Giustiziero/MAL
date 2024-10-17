import React from 'react';
import { Box, Image, Text } from 'grommet';

const AnimeDetails = ({ details }) => {
  if (!details) return null;

  const { main_picture, mean, genres, synopsis, title } = details;
  const largeImageUrl = main_picture?.large;

  const genreNames = genres.map(genre => genre.name);

  return (
    <Box direction="row" pad="medium" background="light-1" round="small" margin={{ top: 'medium' }} className="anime-details-box">
      {/* Anime Image */}
      <Box flex={{ shrink: 0 }} margin={{ right: 'medium' }}>
        {/* Set fit="contain" to avoid cropping and adjust layout */}
        <Image src={largeImageUrl} fit="contain" style={{ maxHeight: '300px', width: 'auto' }} />
      </Box>

      
      {/* Anime Details */}
      <Box flex>
        {/* Bold Anime Title */}
        <Text weight="bold" size="large">{title}</Text>  {/* Display title with bold styling */}

        {/* Score without bold */}
        <Text>Score: {mean}</Text>  {/* No bold styling here */}

        {/* Genres */}
        <Text>Genres: {genreNames.join(', ')}</Text>

        {/* Synopsis */}
        <Text margin={{ top: 'small' }}>Synopsis:</Text>
        <Text size="small">{synopsis}</Text>
      </Box>
    </Box>
  );
};

export default AnimeDetails;
