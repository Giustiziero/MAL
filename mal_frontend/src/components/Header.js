// src/components/Header.js

import React from 'react';
import { Box, Text, Anchor } from 'grommet';

const Header = () => {
  return (
    <Box
      direction="row"
      align="center"
      justify="between"
      pad={{ vertical: 'small', horizontal: 'medium' }}
      background="brand"
      style={{ alignSelf: "center", width: '100%', margin: "auto" }}
    >
      <Box width="1060px" margin={{ left: 'auto', right: 'auto' }} direction='row' justify="between" align="center">
        <Text className="logo" size="large" weight="bold" color="white">
          MyAnimeRecs
        </Text>
        <Box className='topnav' direction='row' >
            <Anchor href="/" label="Anime-Based Rec" />
            <Anchor href="/about" label="About" />
        </Box>
      </Box>
    </Box>
  );
};

export default Header;
