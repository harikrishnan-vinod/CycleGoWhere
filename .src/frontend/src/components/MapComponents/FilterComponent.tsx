import { useState } from "react";
import "../../components.css/MapComponents/FilterComponents.css";

interface FilterComponentProps {
  showWater: boolean;
  setShowWater: (show: boolean) => void;
  showRepair: boolean;
  setShowRepair: (show: boolean) => void;
  showPark: boolean;
  setShowPark: (show: boolean) => void;
}

function FilterComponent({
  showWater,
  setShowWater,
  showRepair,
  setShowRepair,
  showPark,
  setShowPark,
}: FilterComponentProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="filter-container">
      <div className="filter-header" onClick={() => setIsOpen(!isOpen)}>
        <h3>Filters {isOpen ? "▲" : "▼"}</h3>
      </div>

      {isOpen && (
        <div className="filter-options">
          <button
            onClick={() => setShowWater(!showWater)}
            className={`filter-button ${showWater ? "active" : "inactive"}`}
          >
            Toggle Water
          </button>
          <button
            onClick={() => setShowRepair(!showRepair)}
            className={`filter-button ${showRepair ? "active" : "inactive"}`}
          >
            Toggle Repair
          </button>
          <button
            onClick={() => setShowPark(!showPark)}
            className={`filter-button ${showPark ? "active" : "inactive"}`}
          >
            Toggle Park
          </button>
        </div>
      )}
    </div>
  );
}

export default FilterComponent;
