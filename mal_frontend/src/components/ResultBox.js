import React, { useState } from 'react';

// const ResultBox = ({ recList }) => {
//     console.log(recList)

//     if (!recList || Object.keys(recList).length === 0) {
//         return <div>No data available</div>;
//     }

//     const recommendations = Object.keys(recList);
//     const rows = Object.values(recList);

//     return (
//         <div>
//             {recommendations.map((recommendation, index) => {
//                 return <p>{index + 1}. {recommendation}: {rows[index]}</p>
//             })}
//         </div>
//     );
// }

const ResultBox = ({ recList }) => {
    console.log(recList);
  
    if (!recList || recList.length === 0) {
      return <div>No data available</div>;
    }
  
    return (
      <div>
        <table>
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
      </div>
    );
  };
  




export default ResultBox