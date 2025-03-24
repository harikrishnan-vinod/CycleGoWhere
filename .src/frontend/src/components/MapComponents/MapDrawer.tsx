import { useState } from "react";
import "../../components.css/MapComponents/MapDrawer.css";

export default function MapDrawer() {
  interface searchData {
    fromAddress: string;
    destAddress: string;
  }

  const [isOpen, setIsOpen] = useState(false);

  const [formData, setFormData] = useState<searchData>({
    fromAddress: "",
    destAddress: "",
  });

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));

    try {
      const url = new URL("http://127.0.0.1:1234/search");
      url.searchParams.append(name, value); // sends only the changed field

      console.log("Sending GET request to:", url.toString());
      const response = await fetch(url.toString(), {
        method: "GET",
      });
      if (!response.ok) {
        throw new Error("Failed to fetch");
      }
      const data = await response.json();
    } catch (Error) {
      console.error(`GET request error for ${name}:`, Error);
    }
  };

  const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      if (formData.fromAddress) {
        params.append("fromAddress", formData.fromAddress);
      }
      if (formData.destAddress) {
        params.append("destAddress", formData.destAddress);
      }

      const url = new URL("http://127.0.0.1:1234/search");
      url.search = params.toString();

      const response = await fetch(url, {
        method: "GET",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Something went wrong");
      }
      console.log("Route response:", data);
    } catch (error) {
      console.error("Submit error:", error);
    }
  };

  return (
    <>
      {!isOpen && (
        <div className="pull-tab" onClick={() => setIsOpen(true)}>
          <div className="drag-bar" />
        </div>
      )}

      <div className={`drawer ${isOpen ? "open" : ""}`}>
        <div className="drag-bar" onClick={() => setIsOpen(false)} />
        <div className="drawer-content">
          <div>
            <input
              name="fromAddress"
              className="search"
              placeholder="Current Location"
              value={formData.fromAddress}
              onChange={handleChange}
            />
            <input
              name="destAddress"
              className="search"
              placeholder="Destination Address"
              value={formData.destAddress}
              onChange={handleChange}
            />
            <button type="button" className="go-button" onClick={handleSubmit}>
              GO
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
