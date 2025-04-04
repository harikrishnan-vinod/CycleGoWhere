import "../components-css/savedRoute.css";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef } from "react";
import L from "leaflet";
import saveicon from "../assets/save.png";

function SavedRoute({ route }: { route: any }) {
  const navigate = useNavigate();
  const mapRef = useRef<HTMLDivElement | null>(null);
  const leafletMapRef = useRef<L.Map | null>(null);

  const handleStart = () => {
    const userUID = sessionStorage.getItem("userUID");
    if (!userUID) return;

    const instructionsArrayFormat = route.instructions.map((inst: any) => [
      inst.direction,
      inst.distance,
      inst.road,
      inst.latLng,
    ]);

    sessionStorage.setItem(
      "savedRouteToStart",
      JSON.stringify({
        route_geometry: route.route_geometry,
        route_instructions: instructionsArrayFormat,
        distance: route.distance,
        startPostal: route.startPostal,
        endPostal: route.endPostal,
        routePath: route.routePath,
        routeId: route.id,
      })
    );

    fetch(
      `http://127.0.0.1:1234/update-last-used?userUID=${userUID}&routeId=${route.id}`,
      { method: "POST" }
    );

    navigate("/MainPage");
  };

  useEffect(() => {
    if (
      !mapRef.current ||
      leafletMapRef.current ||
      !Array.isArray(route.routePath) ||
      route.routePath.length === 0
    ) {
      return;
    }

    leafletMapRef.current = L.map(mapRef.current, {
      center: L.latLng(1.35, 103.8),
      zoom: 12,
      zoomControl: false,
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: false,
      boxZoom: false,
      keyboard: false,
      touchZoom: false,
      attributionControl: false,
    });

    L.tileLayer(
      "https://www.onemap.gov.sg/maps/tiles/Default/{z}/{x}/{y}.png",
      {
        detectRetina: true,
        maxZoom: 19,
        minZoom: 11,
      }
    ).addTo(leafletMapRef.current);

    const latlngs = route.routePath.map((pt: any) =>
      L.latLng(pt.latitude, pt.longitude)
    );
    const poly = L.polyline(latlngs, { color: "blue", weight: 4 }).addTo(
      leafletMapRef.current
    );
    leafletMapRef.current.fitBounds(poly.getBounds());
  }, [route]);

  let lastUsedStr = "Not used yet";

  if (route.lastUsedAt) {
    try {
      const date =
        typeof route.lastUsedAt === "string"
          ? new Date(route.lastUsedAt)
          : new Date(route.lastUsedAt.seconds * 1000);
      lastUsedStr = date.toLocaleString();
    } catch {
      lastUsedStr = "Invalid date";
    }
  }
  const handleUnsave = async () => {
    // Ask the user for confirmation
    const isConfirmed = window.confirm("Are you sure you want to unsave this activity?");

    if (isConfirmed) {
      const userUID = sessionStorage.getItem("userUID");

      if (!userUID) {
        alert("User not logged in");
        return;
      }

      try {
        const res = await fetch("http://127.0.0.1:1234/unsave-route", {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userUID, routeId: route.id }), // Assuming `route.id` is the unique identifier
        });

        if (res.ok) {
          alert("Route unsaved successfully!");
          // After unsaving the route, refresh the page
          window.location.reload(); // This refreshes the page to show the updated state
        } else {
          alert("Failed to unsave route.");
        }
      } catch (err) {
        console.error("Error unsaving route:", err);
        alert("Error unsaving route.");
      }
    } else {
      // If the user cancels, do nothing
      console.log("Unsave action cancelled.");
    }
  };



  return (
    <div className="saved-activity-container">
      <div className="saved-activity-top">
        <div className="saved-activity-title">
          <h2>{route.routeName}</h2>
        </div>
        <div className="saved-activity-description">{route.notes}</div>
        <div className="saved-activity-last-used">
          <p>Last Used: {lastUsedStr}</p>
        </div>
      </div>

      <div
        className="saved-activity-map"
        ref={mapRef}

      />

      <div className="saved-activity-details">
        <div className="saved-activity-distance">
          <p>Distance: {(route.distance / 1000).toFixed(2)} km</p>
        </div>
        <div>
          <button
            className="start-activity-from-route-btn"
            onClick={handleStart}
          >
            Start Activity
          </button>

          <div onClick={handleUnsave}>
            <img className="unsave-activity-btn" src={saveicon} alt="Unsave" />
          </div>

        </div>
      </div>
    </div >
  );
}

export default SavedRoute;
