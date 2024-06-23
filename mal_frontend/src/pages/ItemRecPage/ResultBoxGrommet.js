import React from 'react';
import { Box, Table, TableBody, TableCell, TableHeader, TableRow, Text } from 'grommet';
import '../../App.css';

const ResultBox = ({ recList }) => {
  console.log(recList);

  if (!recList || recList.length === 0) {
    return (
      <Box pad="medium" background="light-2" round="small" margin={{ top: 'medium' }} align="center">
        <Text>No data available</Text>
      </Box>
    );
  }

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
                <td>{recommendation}</td>
                <td>{value}</td>
                </tr>
            ))}
            </tbody>
        </table>
    </Box>
  );
};

export default ResultBox;
