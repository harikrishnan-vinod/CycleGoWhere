import { useState, useEffect, useRef } from "react";
import "../components-css/cyclingActivity.css";
import L from "leaflet";
import SaveIcon from "../assets/savedroutesicon.png";
import SaveRouteModal from "./MapComponents/SaveRouteModal";
import polyline from "@mapbox/polyline";
import deleteicon from "../assets/delete.png";

interface ActivityProps {
  activity: any;
}

function CyclingActivity({ activity }: ActivityProps) {
  const [username, setUsername] = useState<string | null>(null);
  const mapRef = useRef<HTMLDivElement | null>(null);
  const leafletMapRef = useRef<L.Map | null>(null);

  const [showModal, setShowModal] = useState(false);
  const [modalRouteName, setModalRouteName] = useState("");
  const [modalNotes, setModalNotes] = useState("");

  const timeTaken = activity?.duration || activity?.timeTaken || 0;
  const distance = activity?.distance || 0;
  const activityName = activity?.activityName || "Untitled Ride";
  const startTimeRaw = activity?.startTime || activity?.createdAt;
  const startTimeStr = startTimeRaw
    ? new Date(startTimeRaw).toLocaleString()
    : "Date not available";

  const formatDuration = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${String(h).padStart(2, "0")}:${String(m).padStart(
      2,
      "0"
    )}:${String(s).padStart(2, "0")}`;
  };



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

    const latlngs = activity.routePath.map((gp: any) =>
      L.latLng(gp.latitude, gp.longitude)
    );
    const poly = L.polyline(latlngs, { color: "blue", weight: 4 }).addTo(
      leafletMapRef.current
    );
    leafletMapRef.current.fitBounds(poly.getBounds());
  }, [activity]);

  const handleSaveRoute = async () => {
    const userUID = sessionStorage.getItem("userUID");

    const latlngArray = activity.routePath?.map((pt: any) => [
      pt.latitude,
      pt.longitude,
    ]);

    if (!latlngArray || latlngArray.length === 0) {
      alert("No route path available to save.");
      return;
    }

    const encodedPolyline = polyline.encode(latlngArray, 5);

    const routeData = {
      routeName: modalRouteName,
      notes: modalNotes,
      distance,
      startPostal: activity.startPostal,
      endPostal: activity.endPostal,
      route_geometry: encodedPolyline,
      route_instructions: activity.instructions,
    };

    try {
      const res = await fetch("http://127.0.0.1:1234/save-route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userUID, routeData }),
      });

      if (res.ok) {
        alert("Route saved successfully!");
        setShowModal(false);
        setModalRouteName("");
        setModalNotes("");
      } else {
        alert("Failed to save route.");
      }
    } catch (err) {
      console.error("Error saving route:", err);
      alert("Error saving route.");
    }


  };
  const handleDeleteActivity = async () => {
    const isConfirmed = window.confirm("Are you sure you want to delete this activity?");

    if (isConfirmed) {
      const userUID = sessionStorage.getItem("userUID");
      console.log("activity.id:", activity.id);


      if (!userUID || !activity.id) {
        alert("Missing user ID or activity ID.");
        return;
      }

      try {
        const res = await fetch("http://127.0.0.1:1234/delete-activity", {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            userUID,
            activityId: activity.id
          }),
        });

        const data = await res.json();

        if (res.ok) {
          alert("Activity deleted successfully!");
          window.location.href = "/Profile";
        } else {
          alert(data.error || "Failed to delete activity.");
        }
      } catch (err) {
        console.error("Error deleting activity:", err);
        alert("Error deleting activity.");
      }
    } else {
      console.log("Delete action cancelled.");
    }
  };
  return (
    <div className="activity-container">
      <div className="activity-header">
        <div className="activity-title">{activityName}</div>
        <div className="activity-notes">
          <p>{activity.notes}</p>
        </div>
        <div className="activity-date">{startTimeStr}</div>
      </div>

      <div className="map-activity" ref={mapRef} />

      <div className="activity-bottom">
        <p className="activity-distance">Distance: {(distance / 1000).toFixed(2)} km</p>
        <div className="action-button">
          <div className="save-activity">
            <img
              onClick={() => {
                setModalRouteName(activity.activityName || "Untitled Route");
                setModalNotes(activity.notes || "");
                setShowModal(true);
              }}
              src={SaveIcon}
              alt="Save Route"
            />
          </div>
          <img className="delete-activity" src={deleteicon} alt="Delete Activity" onClick={handleDeleteActivity} title="Delete This Activity" />
        </div>

      </div>


      {showModal && (
        <SaveRouteModal
          routeName={modalRouteName}
          notes={modalNotes}
          onNameChange={setModalRouteName}
          onNotesChange={setModalNotes}
          onConfirm={handleSaveRoute}
          onCancel={() => setShowModal(false)}
        />
      )}
    </div>
  );
}

export default CyclingActivity;
