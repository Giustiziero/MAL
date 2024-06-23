import React from 'react';
import { Grommet } from 'grommet';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import ItemRec from './pages/ItemRecPage/ItemRec';
import About from './pages/AboutPage/About';
import './App.css';

const theme = {
  global: {
    font: {
      family: 'Arial',
      size: '14px',
      height: '20px',
    },
    colors: {
      brand: '#00739D',
    },
  },
};

const App = () => (
  <Grommet theme={theme} full className="main">
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<ItemRec />}/>
        <Route path="/about" element={<About />}  />
      </Routes>
    </Router>
  </Grommet>
);

export default App;
