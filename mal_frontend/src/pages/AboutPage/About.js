import React from 'react';
import { Box, Heading, Text, Anchor, Image, List } from 'grommet';
import { MailOption, Github, Linkedin } from 'grommet-icons';  // Import GitHub and LinkedIn icons

const About = () => (
  <Box align="center" justify="center" fill background="dark-1" pad="large" gap="medium">
    {/* Banner or Project Logo */}
    <Box height="small" width="medium" margin={{ bottom: 'medium' }}>
      <Image fit="cover" src="/banner.png" alt="Project Banner" />
    </Box>

    {/* Project Description */}
    <Box width="large" pad="small" align="center">
      <Heading level={2} color='light-2'>Welcome to the Anime Recommendation Project</Heading>
      <Text size="large" color="light-4" textAlign="center" margin={{ vertical: 'small' }}>
        This project was created with the purpose of developing a better recommendation algorithm for animes 
        based on what <strong>MyAnimeList</strong> users have demonstrated. Currently, the only recommendations 
        that exist are based on user reviews suggesting other animes.
      </Text>
      <Anchor href="https://kind-sand-08ef48010.5.azurestaticapps.net/" color="light-1" label="Visit Current Website" />
    </Box>

    {/* Frontend and Backend Overview */}
    <Box width="large" pad="small" align="center" margin={{ top: 'medium' }}>
      <Heading level={3} color='light-3'>Project Architecture</Heading>
      <Text size="medium" color="light-4" textAlign="center" margin={{ bottom: 'small' }}>
        The project is divided into two main parts:
      </Text>

      {/* Frontend */}
      <Box pad="small" background="dark-2" round="small" margin={{ bottom: 'small' }}>
        <Heading level={4} color='light-3'>Frontend</Heading>
        <Text size="medium" color="light-4" textAlign="center">
          The frontend was created using React and is currently hosted by Azure Static Web Services. 
          It provides a user-friendly interface for interacting with the recommendation system.
        </Text>
      </Box>

      {/* Backend */}
      <Box pad="small" background="dark-2" round="small" margin={{ bottom: 'small' }}>
        <Heading level={4} color='light-3'>Backend</Heading>
        <Text size="medium" color="light-4" textAlign="center">
          The backend is entirely written in Python and hosted on Azure. It handles the logic for 
          fetching and processing data from the MyAnimeList APIs and running the recommendation algorithm.
        </Text>
      </Box>

      {/* Algorithm */}
      <Box pad="small" background="dark-2" round="small">
        <Heading level={4} color='light-3'>Recommendation Algorithm</Heading>
        <Text size="medium" color="light-4" textAlign="center">
          The algorithm currently uses content-based collaborative filtering based on user reviews. 
          User data is sourced from both the official and unofficial MyAnimeList APIs and is stored in an Azure Cosmos (NoSQL) database.
        </Text>
      </Box>
    </Box>

    {/* Future Features */}
    <Box width="large" pad="small" align="center" margin={{ top: 'medium' }}>
      <Heading level={3} color='light-3'>Future Features</Heading>
      <Text size="medium" color="light-4" textAlign="center" margin={{ bottom: 'small' }}>
        Planned improvements for the project:
      </Text>
      <List
        primaryKey="feature"
        data={[
          { feature: 'User-based collaborative filtering based on user’s MyAnimeList account' },
          { feature: 'Recommendations based on written review content using a bag of words model' },
          { feature: 'Improved database and API integration for faster and more scalable results' }
        ]}
        border={false}
        pad="small"
        background="dark-2"
        round="small"
        gap="small"
      />
    </Box>

    {/* Contact / Call to Action */}
    <Box pad="small" align="center" margin={{ top: 'medium' }}>
      <Text size="medium" color="light-4" margin={{ bottom: 'small' }}>Reach out if you're interested in contributing to the project!</Text>

      {/* Contact Options in a Row */}
      <Box direction="row" gap="medium" align="center" justify="center">
        {/* Email */}
        <Anchor href="mailto:youremail@example.com" icon={<MailOption color="light-1" />} label="Email" />
        
        {/* GitHub */}
        <Anchor href="https://github.com/yourusername/yourproject" icon={<Github color="light-1" />} label="GitHub" />
        
        {/* LinkedIn */}
        <Anchor href="https://www.linkedin.com/in/yourusername" icon={<Linkedin color="light-1" />} label="LinkedIn" />
      </Box>
    </Box>
  </Box>
);

export default About;
