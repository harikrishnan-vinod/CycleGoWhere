import { useState, useEffect, useRef } from "react";
import "../components-css/cyclingActivity.css";
import { Camera } from "lucide-react";
import { Link } from "react-router-dom";
import L from "leaflet";
import polyline from "@mapbox/polyline";

interface ActivityProps {
  activity: any;
}

function CyclingActivity({ activity }: ActivityProps) {
  const [username, setUsername] = useState<string | null>(null);
  const mapRef = useRef<HTMLDivElement | null>(null);
  const leafletMapRef = useRef<L.Map | null>(null);

  // decode geometry if present
  const routeGeometry =
    activity?.route_geometry || activity?.route_geometryString;
  const timeTaken = activity?.duration || activity?.timeTaken || 0;

  const formatDuration = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${String(h).padStart(2, "0")}:${String(m).padStart(
      2,
      "0"
    )}:${String(s).padStart(2, "0")}`;
  };

  const distance = activity?.distance || 0;
  const activityName = activity?.activityName || "Untitled Ride";
  const notes = activity?.notes || "";
  const startTimeSec =
    activity?.startTime?.seconds || activity?.createdAt?.seconds || 0;
  const startTimeObj = new Date(startTimeSec * 1000);
  const startTimeStr = startTimeSec
    ? startTimeObj.toLocaleString()
    : "Date not available";

  useEffect(() => {
    const displayUsername = async () => {
      const userUID = sessionStorage.getItem("userUID");
      if (!userUID) return;
      try {
        const usernameResponse = await fetch(
          `http://127.0.0.1:1234/get-username?userUID=${userUID}`
        );
        const usernameResult = await usernameResponse.json();
        if (usernameResponse.ok && usernameResult.username) {
          setUsername(usernameResult.username);
        }
      } catch (err) {
        console.error("Error fetching profile data:", err);
      }
    };
    displayUsername();
  }, []);

  // Setup a small Leaflet map for the route
  useEffect(() => {
    if (
      !mapRef.current ||
      leafletMapRef.current ||
      !Array.isArray(activity.routePath) ||
      activity.routePath.length === 0
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

    const latlngs = activity.routePath.map(
      (gp: any) => L.latLng(gp.latitude, gp.longitude) // uses the newly serialized lat/lng
    );

    const poly = L.polyline(latlngs, { color: "blue", weight: 4 }).addTo(
      leafletMapRef.current
    );
    leafletMapRef.current.fitBounds(poly.getBounds());
  }, [activity]);
  return (
    <div className="activity-container">
      <div className="activity-header">
        <div className="activity-title">{activityName}</div>
        <div className="activity-date">{startTimeStr}</div>
      </div>

      <div className="map-activity" ref={mapRef} />

      <div className="activity-statistics">
        <div className="distance">
          <p>Distance: {distance} m</p>
        </div>
        <div className="duration">
          <p>Duration: {formatDuration(timeTaken)}</p>
        </div>
        <div className="average-speed">
          <p>Avg Speed: {(distance / timeTaken || 0).toFixed(2)} m/s</p>
        </div>
      </div>

      <div style={{ padding: "0.5rem 1rem" }}>
        <p style={{ margin: 0 }}>{notes}</p>
      </div>

      <div className="actions-activity">
        <div className="save-activity">{/* example icon or link */}</div>
        <div className="delete-activity">{/* example icon or link */}</div>
      </div>
    </div>
  );
}

export default CyclingActivity;
