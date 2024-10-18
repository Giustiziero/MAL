import React from 'react';
import { Box, Heading, Text, Anchor, Image } from 'grommet';
import { MailOption, Github, Linkedin } from 'grommet-icons';  // Import GitHub and LinkedIn icons

const About = () => (
  <Box fill align="center" justify="center" pad="large">  {/* Center the entire page content */}
    
    {/* Image Section wrapped in its own Box */}
    <Box className='center-column'>
      <Box height="auto" width="auto" align="center" overflow="hidden" pad={{top:"none", bottom:"none", left:"large", right:"large"}} style={{ position: 'relative' }}>
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
    </Box>

    {/* Content Pillar */}
    <Box className='content-pillar'
      width="xlarge"  // Set the width of the content pillar
      pad="medium"  // Reduce padding to make it tighter
      round="small"
      align="center"
      background={{ color: 'rgba(255, 255, 255, 0.9)' }}  // Light background for contrast
      style={{ boxShadow: '0px 0px 15px rgba(0, 0, 0, 0.2)' }}  // Shadow for visual depth
    >
      
      {/* Project Description */}
      <Heading level={2} color="black" size="large" margin="small" textAlign="center">
        Welcome to the Anime Recommendation Project
      </Heading>
      <Text size="large" color="black" textAlign="justify" margin={{ vertical: 'small' }}>
        This project was created with the purpose of developing a better recommendation algorithm for animes 
        based on what <Anchor href="https://myanimelist.net/" label="MyAnimeList" color="black" /> users have demonstrated. Currently, the only recommendations 
        that exist are based on specific suggestions made by other users, which are often lacking. 
      </Text>

      {/* Frontend and Backend Overview */}
      <Box pad="small" align="center" margin={{ top: 'medium' }}>
        <Heading level={3} color="black">Project Architecture</Heading>
        <Text size="medium" color="black" textAlign="center" margin={{ bottom: 'small' }}>
          The project is divided into two main parts:
        </Text>

        {/* Frontend */}
        <Box pad="medium" round="small" margin={{ bottom: 'small' }} background={{ color: 'rgba(255, 255, 255, 0.9)' }} border={{ color: 'black', size: 'small' }} width="large">
          <Heading level={4} color="black">Frontend</Heading>
          <Text size="medium" color="black" textAlign="justify">
            The frontend was created using React and is currently hosted by Azure Static Web Services. 
            It provides a user-friendly interface for interacting with the recommendation system.
          </Text>
        </Box>

        {/* Backend */}
        <Box pad="medium" round="small" margin={{ bottom: 'small' }} background={{ color: 'rgba(255, 255, 255, 0.9)' }} border={{ color: 'black', size: 'small' }} width="large">
          <Heading level={4} color="black">Backend</Heading>
          <Text size="medium" color="black" textAlign="justify">
            The backend is entirely written in Python and hosted on Azure. It handles the logic for 
            fetching and processing data from the MyAnimeList APIs and running the recommendation algorithm.
          </Text>
        </Box>

        {/* Algorithm */}
        <Box pad="medium" round="small" background={{ color: 'rgba(255, 255, 255, 0.9)' }} border={{ color: 'black', size: 'small' }} width="large">
          <Heading level={4} color="black">Recommendation Algorithm</Heading>
          <Text size="medium" color="black" textAlign="justify">
            The algorithm currently uses content-based collaborative filtering based on user reviews. 
            User data is sourced from both the official and unofficial MyAnimeList APIs and is stored in an Azure Cosmos (NoSQL) database.
          </Text>
        </Box>
      </Box>

      {/* Future Features */}
      <Box width="large" pad="medium" align="center" margin={{ top: 'medium' }} background={{ color: 'rgba(255, 255, 255, 0.9)' }} round="small">
        <Heading level={3} color="black">Future Features</Heading>
        <Text size="medium" color="black" textAlign="center" margin={{ bottom: 'small' }}>
          Planned improvements for the project:
        </Text>

        {/* Features as Bullet Points */}
        <Box as="ul" margin="none" pad="small">
          <li>
            <Text size="medium" color="black" margin="none" pad="none">
              User-based collaborative filtering based on user’s MyAnimeList account.
            </Text>
          </li>
          <li>
            <Text size="medium" color="black" margin="none" pad="none">
              Collapsible view of anime details inside the recommendation box.
            </Text>
          </li>
          <li>
            <Text size="medium" color="black" margin="none" pad="none">
              Sentiment analysis and recommendation based on written user reviews of anime using NLP and possibly pre-trained LLMs.
            </Text>
          </li>
        </Box>
      </Box>

      {/* Contact / Call to Action */}
      <Box pad="small" align="center" margin={{ top: 'medium' }}>
        <Text size="medium" color="black" margin={{ bottom: 'small' }}>Reach out if you're interested in contributing to the project!</Text>

        {/* Contact Options in a Row */}
        <Box direction="row" gap="medium" align="center" justify="center">
          {/* Email */}
          <Anchor href="mailto:giuliano_tissot@hotmail.com" icon={<MailOption color="black" />} label="Email" />
          
          {/* GitHub */}
          <Anchor href="https://github.com/Giustiziero/MAL" icon={<Github color="black" />} label="GitHub" />
          
          {/* LinkedIn */}
          <Anchor href="https://www.linkedin.com/in/giuliano-tissot-1432508b/" icon={<Linkedin color="black" />} label="LinkedIn" />
        </Box>
      </Box>

    </Box>
  </Box>
);

export default About;
