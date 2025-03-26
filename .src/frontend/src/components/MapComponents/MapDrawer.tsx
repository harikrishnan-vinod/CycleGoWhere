import { useState } from "react";
import "../../components.css/MapComponents/MapDrawer.css";

interface MapDrawerProps {
  setRouteGeometry: (geometry: string) => void;
  clearRoute: () => void;
  setRouteInstructions: (routeInstructions: any) => void;
}

interface searchData {
  fromAddress: string;
  destAddress: string;
}

export default function MapDrawer({
  setRouteGeometry,
  clearRoute,
  setRouteInstructions,
}: MapDrawerProps) {
  const [isOpen, setIsOpen] = useState(true); // open by default

  const [formData, setFormData] = useState<searchData>({
    fromAddress: "",
    destAddress: "",
  });

  const [fromSuggestions, setFromSuggestions] = useState<any[]>([]);
  const [destSuggestions, setDestSuggestions] = useState<any[]>([]);

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));

    if (!value.trim()) {
      if (name === "fromAddress") {
        setFromSuggestions([]);
      } else {
        setDestSuggestions([]);
      }
      return;
    }

    try {
      const url = new URL("http://127.0.0.1:1234/search");
      url.searchParams.append(name, value);

      const response = await fetch(url.toString());
      if (!response.ok) throw new Error("Failed to fetch suggestions");

      const data = await response.json();
      const trimmedResults = data.results.slice(0, 5);

      if (name === "fromAddress") {
        setFromSuggestions(trimmedResults);
      } else {
        setDestSuggestions(trimmedResults);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    clearRoute();
    setRouteInstructions(null);

    try {
      const url = new URL("http://127.0.0.1:1234/route");
      url.searchParams.append("fromAddress", formData.fromAddress);
      url.searchParams.append("destAddress", formData.destAddress);

      const response = await fetch(url.toString());
      if (!response.ok) throw new Error("Failed to fetch route");

      const data = await response.json();
      setRouteGeometry(data.route_geometry);
      setRouteInstructions(data.route_instructions);
    } catch (error) {
      console.log("Submit error:", error);
    }
  };

  return (
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

      {/* Drag bar at the BOTTOM of the drawer */}
      <div className="drag-bar" onClick={() => setIsOpen(!isOpen)} />
    </div>
  );
}
