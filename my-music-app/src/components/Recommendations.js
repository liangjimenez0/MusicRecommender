import React from "react";

const Recommendations = ({ recommendations }) => {
  return (
    <div className="recommendations">
      {recommendations.length > 0 && (
        <div>
          <h3 className="recommendations-title">Recommendations</h3>
          <ul className="recommendations-list">
            {recommendations.map((rec, index) => (
              <li className="recommendations-item" key={index}>
                <span className="bold">{rec.track_name}</span> by {rec.artists}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Recommendations;
