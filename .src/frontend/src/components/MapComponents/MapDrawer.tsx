import { useState } from "react";
import "../../components.css/MapComponents/MapDrawer.css";
import { useForm } from "../../hooks/useForm";

export default function MapDrawer() {
  // interface Location {
  //   name: string;
  //   postalcode: string;
  //   distance: string;
  //   time: string;
  // }

  const [isOpen, setIsOpen] = useState(false);

  const { form, handleChange } = useForm({
    destAddress: "",
    fromAddress: "",
  });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:1234/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          startingAddress: form.fromAddress,
          destinationAddress: form.destAddress,
        }),
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
          <form onSubmit={handleSubmit}>
            <input
              name="fromAddress"
              className="search"
              placeholder="Current Location"
              value={form.fromAddress}
              onChange={handleChange}
            />
            <input
              name="destAddress"
              className="search"
              placeholder="Destination Address"
              value={form.destAddress}
              onChange={handleChange}
            />
            <button type="submit" className="go-button">
              GO
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
