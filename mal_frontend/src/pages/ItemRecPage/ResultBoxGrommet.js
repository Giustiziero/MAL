import React from 'react';
import { Box, Text } from 'grommet';
import '../../App.css';

const ResultBox = ({ recList, onSearch }) => {
  console.log(recList);

  if (!recList || recList.length === 0) {
    return (
      <Box pad="medium" background="light-2" round="small" margin={{ top: 'medium' }} align="center">
        <Text>No data available</Text>
      </Box>
    );
  }

  const handleClick = (animeName) => {
    // Trigger a new search for the selected anime
    onSearch(animeName);
  };

  return (
    <Box className="result-box" >
        <table className="result-table">
            <thead>
            <tr>
                <th>#</th>
                <th>Recommendation</th>
                <th>Value</th>
            </tr>
            </thead>
            <tbody>
            {recList.map(([recommendation, value], index) => (
                <tr key={index}>
                <td>{index + 1}</td>
                <td>
                  <button
                    onClick={() => handleClick(recommendation)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: 'darkblue',
                      textDecoration: 'none',
                      cursor: 'pointer',
                    }}
                    >
                    {recommendation}
                  </button>

                </td>
                <td>{value}</td>
                </tr>
            ))}
            </tbody>
        </table>
    </Box>
  );
};

export default ResultBox;
