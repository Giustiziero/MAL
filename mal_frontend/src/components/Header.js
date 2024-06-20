// src/components/Header.js

import React from 'react';
import { Box, Text } from 'grommet';

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
      <Box width="1060px" margin={{ left: 'auto', right: 'auto' }}>
        <Text size="large" weight="bold" color="white">
          Anime Recs
        </Text>
      </Box>
    </Box>
  );
};

export default Header;
