import { useState, useImperativeHandle, forwardRef } from "react";
import "../../components.css/MapComponents/MapDrawer.css";
import { SearchData, RouteSummary } from "../../types";

interface MapDrawerProps {
  setRouteGeometry: (geometry: string) => void;
  clearRoute: () => void;
  setRouteInstructions: (instructions: any[]) => void;
  setWaterPoints: (points: any[]) => void;
  setRouteMeta: (dist: number, startPost: string, endPost: string) => void;
  mapInstance: L.Map | null;
  setRouteSummary: (summary: RouteSummary) => void;
  setRepairPoints: (points: any[]) => void;
  setParkPoints: (points: any[]) => void;
  startOpen?: boolean;
}

export type MapDrawerRef = {
  resetInputs: () => void;
  loadSavedRoute: (
    geometry: string,
    instructions: any[],
    summary: RouteSummary,
    startPostal: string,
    endPostal: string
  ) => void;
};

const MapDrawer = forwardRef<MapDrawerRef, MapDrawerProps>((props, ref) => {
  const {
    setRouteGeometry,
    clearRoute,
    setRouteInstructions,
    setWaterPoints,
    setRouteMeta,
    setRouteSummary,
    setRepairPoints,
    setParkPoints,
    startOpen,
  } = props;

  const [isOpen, setIsOpen] = useState(startOpen ?? true);
  const [formData, setFormData] = useState<SearchData>({
    fromAddress: "",
    destAddress: "",
  });
  const [fromSuggestions, setFromSuggestions] = useState<any[]>([]);
  const [destSuggestions, setDestSuggestions] = useState<any[]>([]);

  useImperativeHandle(ref, () => ({
    resetInputs: () => {
      setFormData({ fromAddress: "", destAddress: "" });
      setFromSuggestions([]);
      setDestSuggestions([]);
    },

    loadSavedRoute: async (
      geometry,
      instructions,
      summary,
      startPostal,
      endPostal
    ) => {
      setIsOpen(false);
      setRouteGeometry(geometry);
      setRouteInstructions(instructions);
      setRouteSummary(summary);

      const water = await fetchWaterPoint(instructions);
      if (water) setWaterPoints(water);

      const shops = await fetchBicycleShop(instructions);
      if (shops) setRepairPoints(shops);

      const parks = await fetchBicyclePark(instructions);
      if (parks) setParkPoints(parks);

      setRouteMeta(summary.total_distance || 0, startPostal, endPostal);
    },
  }));

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    if (!value.trim()) {
      if (name === "fromAddress") setFromSuggestions([]);
      else setDestSuggestions([]);
      return;
    }

    try {
      const url = new URL("http://127.0.0.1:1234/search");
      url.searchParams.append(name, value);
      const response = await fetch(url.toString());
      if (!response.ok) throw new Error("Failed to fetch suggestions");
      const data = await response.json();
      const trimmedResults = data.results.slice(0, 5);
      if (name === "fromAddress") setFromSuggestions(trimmedResults);
      else setDestSuggestions(trimmedResults);
    } catch {}
  };

  const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    clearRoute();
    setRouteInstructions([]);

    if (!formData.fromAddress.trim() || !formData.destAddress.trim()) {
      alert("Please enter both a valid starting point and destination.");
      return;
    }

    try {
      const url = new URL("http://127.0.0.1:1234/route");
      url.searchParams.append("fromAddress", formData.fromAddress);
      url.searchParams.append("destAddress", formData.destAddress);

      const response = await fetch(url.toString());

      if (!response.ok) throw new Error("Failed to fetch route");

      const data = await response.json();

      if (
        !data.route_geometry ||
        !Array.isArray(data.route_instructions) ||
        data.route_instructions.length === 0
      ) {
        alert("Please enter both a valid starting point and destination.");
        return;
      }

      setRouteGeometry(data.route_geometry);
      setRouteInstructions(data.route_instructions);
      setRouteSummary(data.route_summary);
      setIsOpen(false);

      const waterData = await fetchWaterPoint(data.route_instructions);
      if (waterData) setWaterPoints(waterData);

      const bicycleRepairData = await fetchBicycleShop(data.route_instructions);
      if (bicycleRepairData) setRepairPoints(bicycleRepairData);

      const bicycleParkData = await fetchBicyclePark(data.route_instructions);
      if (bicycleParkData) setParkPoints(bicycleParkData);

      if (data.route_summary) {
        setRouteMeta(
          data.route_summary.total_distance || 0,
          data.route_summary.start_postal || formData.fromAddress,
          data.route_summary.end_postal || formData.destAddress
        );
      }
    } catch {
      alert("Please enter both a valid starting point and destination.");
    }
  };

  const fetchWaterPoint = async (instructions: any[]) => {
    try {
      const response = await fetch("http://127.0.0.1:1234/fetchWaterPoint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ routeInstructions: instructions }),
      });
      if (!response.ok)
        throw new Error(`HTTP error! Status: ${response.status}`);
      return await response.json();
    } catch {}
  };

  const fetchBicycleShop = async (instructions: any[]) => {
    try {
      const response = await fetch("http://127.0.0.1:1234/fetchBicycleShop", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ routeInstructions: instructions }),
      });
      if (!response.ok)
        throw new Error(`HTTP error! Status: ${response.status}`);
      return await response.json();
    } catch {}
  };

  const fetchBicyclePark = async (instructions: any[]) => {
    try {
      const response = await fetch("http://127.0.0.1:1234/fetchBicyclePark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ routeInstructions: instructions }),
      });
      if (!response.ok)
        throw new Error(`HTTP error! Status: ${response.status}`);
      return await response.json();
    } catch {}
  };

  return (
    <>
      <div className={`drawer ${isOpen ? "open" : ""}`}>
        <div className="drawer-content">
          <input
            name="fromAddress"
            className="search"
            placeholder="Current Location"
            value={formData.fromAddress}
            onChange={handleChange}
          />
          <ul className="suggestions">
            {fromSuggestions.map((item, idx) => (
              <li
                key={idx}
                onClick={() => {
                  setFormData((prev) => ({
                    ...prev,
                    fromAddress: item.ADDRESS,
                  }));
                  setFromSuggestions([]);
                }}
              >
                {item.ADDRESS}
              </li>
            ))}
          </ul>

          <input
            name="destAddress"
            className="search"
            placeholder="Destination Address"
            value={formData.destAddress}
            onChange={handleChange}
          />
          <ul className="suggestions">
            {destSuggestions.map((item, idx) => (
              <li
                key={idx}
                onClick={() => {
                  setFormData((prev) => ({
                    ...prev,
                    destAddress: item.ADDRESS,
                  }));
                  setDestSuggestions([]);
                }}
              >
                {item.ADDRESS}
              </li>
            ))}
          </ul>

          <button type="button" className="go-button" onClick={handleSubmit}>
            Show Route
          </button>
        </div>
        <div className="drag-bar" onClick={() => setIsOpen(!isOpen)} />
      </div>
      {!isOpen && startOpen && (
        <div className="pull-tab-closed" onClick={() => setIsOpen(true)} />
      )}
    </>
  );
});

export default MapDrawer;
