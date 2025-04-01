// MapDrawer.tsx
import { useState } from "react";
import "../../components.css/MapComponents/MapDrawer.css";

interface MapDrawerProps {
  setRouteGeometry: (geometry: string) => void;
  clearRoute: () => void;
  setRouteInstructions: (instructions: any[]) => void;
  setWaterPoints: (points: any[]) => void;
  setRouteMeta: (dist: number, startPost: string, endPost: string) => void;
}

interface SearchData {
  fromAddress: string;
  destAddress: string;
}

export default function MapDrawer({
  setRouteGeometry,
  clearRoute,
  setRouteInstructions,
  setWaterPoints,
  setRouteMeta,
}: MapDrawerProps) {
  const [isOpen, setIsOpen] = useState(true);
  const [formData, setFormData] = useState<SearchData>({
    fromAddress: "",
    destAddress: "",
  });
  const [fromSuggestions, setFromSuggestions] = useState<any[]>([]);
  const [destSuggestions, setDestSuggestions] = useState<any[]>([]);

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

    try {
      const url = new URL("http://127.0.0.1:1234/route");
      url.searchParams.append("fromAddress", formData.fromAddress);
      url.searchParams.append("destAddress", formData.destAddress);

      const response = await fetch(url.toString());
      if (!response.ok) throw new Error("Failed to fetch route");
      const data = await response.json();

      setRouteGeometry(data.route_geometry);
      setRouteInstructions(data.route_instructions);

      setIsOpen(false);

      const waterData = await fetchWaterPoint(data.route_instructions);
      if (waterData) setWaterPoints(waterData);

      if (data.route_summary) {
        setRouteMeta(
          data.route_summary.total_distance || 0,
          data.route_summary.start_postal || formData.fromAddress,
          data.route_summary.end_postal || formData.destAddress
        );
      }
    } catch {}
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
            GO
          </button>
        </div>
        <div className="drag-bar" onClick={() => setIsOpen(!isOpen)} />
      </div>
      {!isOpen && (
        <div className="pull-tab-closed" onClick={() => setIsOpen(true)} />
      )}
    </>
  );
}
