import React from "react";
import "../../components.css/MapComponents/RouteInstructionList.css";

interface RouteInstructionListProps {
  routeInstructions: any[];
}

const RouteInstructionList: React.FC<RouteInstructionListProps> = ({
  routeInstructions,
}) => {
  if (!routeInstructions || routeInstructions.length === 0) {
    return null;
  }

  return (
    <div className="route-instruction-container">
      <h3>Route Instructions</h3>
      <ol className="route-instruction-list">
        {routeInstructions.map((instruction, index) => (
          <li key={index} className="route-instruction-item">
            <strong>{instruction[9]}</strong>
            <div className="instruction-meta">
              {instruction[1] && <div>Road: {instruction[1]}</div>}
              Distance: {instruction[5]}
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
};

export default RouteInstructionList;
