// RouteInstructionsList.tsx
import { useState, forwardRef } from "react";
import "../../components.css/MapComponents/RouteInstructionList.css";

interface RouteInstructionListProps {
  routeInstructions: any[];
}

// Use React.forwardRef so the parent (BaseMap) can attach a ref
const RouteInstructionsList = forwardRef<
  HTMLDivElement,
  RouteInstructionListProps
>(({ routeInstructions }, ref) => {
  const [isOpen, setIsOpen] = useState(false);

  if (!routeInstructions || routeInstructions.length === 0) {
    return null;
  }

  return (
    <div className="route-instruction-container" ref={ref}>
      <div
        className="route-instruction-header"
        onClick={() => setIsOpen(!isOpen)}
        style={{
          cursor: "pointer",
          background: "#f0f0f0",
          padding: "10px",
        }}
      >
        <h3 style={{ margin: 0 }}>Route Instructions {isOpen ? "▲" : "▼"}</h3>
      </div>

      {isOpen && (
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
      )}
    </div>
  );
});

RouteInstructionsList.displayName = "RouteInstructionsList";

export default RouteInstructionsList;
