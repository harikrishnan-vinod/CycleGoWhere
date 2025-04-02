import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-routing-machine";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import polyline from "@mapbox/polyline";
import Navigate from "../../components/Navigation";
import MapDrawer from "./MapDrawer";
import RouteInstructionsList from "./RouteInstructionsList";
import "../../components.css/MapComponents/BaseMap.css";

function BaseMap() {
  const mapRef = useRef<L.Map | null>(null);
  const polylineLayerRef = useRef<L.Polyline | null>(null);
  const startMarkerRef = useRef<L.Marker | null>(null);
  const endMarkerRef = useRef<L.Marker | null>(null);

  // ROUTE STATES
  const [routeGeometry, setRouteGeometry] = useState<string | null>(null);
  const [routeInstructions, setRouteInstructions] = useState<any[]>([]);
  const [waterPoints, setWaterPoints] = useState<any[]>([]);
  const [distance, setDistance] = useState<number>(0);
  const [startPostal, setStartPostal] = useState("");
  const [endPostal, setEndPostal] = useState("");

  // SAVE ROUTE MODAL
  const [routeModalOpen, setRouteModalOpen] = useState(false);
  const [routeName, setRouteName] = useState("");
  const [notes, setNotes] = useState("");

  // ACTIVITY STATES
  const [activityStarted, setActivityStarted] = useState(false);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  // SAVE ACTIVITY MODAL
  const [activityModalOpen, setActivityModalOpen] = useState(false);
  const [activityName, setActivityName] = useState("");
  const [activityDescription, setActivityDescription] = useState("");

  // MAP SETUP
  useEffect(() => {
    if (mapRef.current) return;
    const sw = L.latLng(1.144, 103.535);
    const ne = L.latLng(1.494, 104.502);
    const bounds = L.latLngBounds(sw, ne);

    const map = L.map("mapdiv", {
      center: L.latLng(1.2868108, 103.8545349),
      zoom: 16,
    });
    map.setMaxBounds(bounds);

    L.tileLayer(
      "https://www.onemap.gov.sg/maps/tiles/Default/{z}/{x}/{y}.png",
      {
        detectRetina: true,
        maxZoom: 19,
        minZoom: 11,
        attribution:
          '<img src="https://www.onemap.gov.sg/web-assets/images/logo/om_logo.png" style="height:20px;width:20px;"/>&nbsp;<a href="https://www.onemap.gov.sg/" target="_blank" rel="noopener noreferrer">OneMap</a>&nbsp;&copy;&nbsp;contributors&nbsp;&#124;&nbsp;<a href="https://www.sla.gov.sg/" target="_blank" rel="noopener noreferrer">Singapore Land Authority</a>',
      }
    ).addTo(map);

    mapRef.current = map;
  }, []);

  // DRAW / REMOVE ROUTE
  useEffect(() => {
    if (!mapRef.current || !routeGeometry) return;
    const latlngs = polyline
      .decode(routeGeometry, 5)
      .map(([lat, lng]) => L.latLng(lat, lng));

    if (polylineLayerRef.current) {
      polylineLayerRef.current.remove();
      polylineLayerRef.current = null;
    }
    if (startMarkerRef.current) {
      startMarkerRef.current.remove();
      startMarkerRef.current = null;
    }
    if (endMarkerRef.current) {
      endMarkerRef.current.remove();
      endMarkerRef.current = null;
    }

    const newPolyline = L.polyline(latlngs, { color: "blue", weight: 5 }).addTo(
      mapRef.current!
    );
    polylineLayerRef.current = newPolyline;

    const startMarker = L.marker(latlngs[0], { title: "Start" }).addTo(
      mapRef.current!
    );
    startMarker.bindPopup("Start").openPopup();
    startMarkerRef.current = startMarker;

    const endMarker = L.marker(latlngs[latlngs.length - 1], {
      title: "Destination",
    }).addTo(mapRef.current!);
    endMarker.bindPopup("Destination");
    endMarkerRef.current = endMarker;

    mapRef.current.fitBounds(newPolyline.getBounds());
  }, [routeGeometry]);

  // WATER POINTS
  useEffect(() => {
    if (!mapRef.current) return;
    waterPoints.forEach((wp) => {
      const marker = L.marker([wp.lat, wp.lng], {
        title: wp.name,
        icon: L.icon({
          iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
          iconSize: [25, 25],
          iconAnchor: [12, 24],
          popupAnchor: [0, -20],
        }),
      }).addTo(mapRef.current!);

      marker.bindPopup(`<b>${wp.name}</b><br/>Distance: ${wp.distance_km} km`);
    });
  }, [waterPoints]);

  // SET ROUTE META
  function handleSetRouteMeta(
    dist: number,
    startPost: string,
    endPost: string
  ) {
    setDistance(dist);
    setStartPostal(startPost);
    setEndPostal(endPost);
  }

  // START/STOP ACTIVITY
  function handleStartActivity() {
    if (!activityStarted) {
      setActivityStarted(true);
      setElapsedSeconds(0);
      timerRef.current = setInterval(() => {
        setElapsedSeconds((prev) => prev + 1);
      }, 1000);
    }
  }

  function handleStopActivity() {
    if (activityStarted) {
      setActivityStarted(false);
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      setActivityModalOpen(true);
    }
  }

  // SAVE ROUTE
  function openRouteModal() {
    setRouteModalOpen(true);
  }

  function closeRouteModal() {
    setRouteModalOpen(false);
  }

  async function handleSaveRoute() {
    const userUID = sessionStorage.getItem("userUID") || "";
    const routeData = {
      routeName,
      notes,
      distance,
      startPostal,
      endPostal,
      route_geometry: routeGeometry,
      route_instructions: routeInstructions,
    };

    try {
      const res = await fetch("http://127.0.0.1:1234/save-route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userUID, routeData }),
      });
      if (res.ok) {
        alert("Route saved successfully");
        setRouteModalOpen(false);
        setRouteName("");
        setNotes("");
      } else {
        alert("Failed to save route");
      }
    } catch {
      alert("Error saving route");
    }
  }

  // END ACTIVITY (clears instructions)
  function handleEndActivity() {
    setRouteInstructions([]);
  }

  // SAVE ACTIVITY
  async function handleConfirmActivity() {
    const userUID = sessionStorage.getItem("userUID") || "";
    const activityData = {
      activityName,
      notes: activityDescription,
      distance,
      route_geometry: routeGeometry,
      route_instructions: routeInstructions,
      startPostal,
      endPostal,
      timeTaken: elapsedSeconds,
    };

    try {
      const res = await fetch("http://127.0.0.1:1234/save-activity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userUID, activityData }),
      });
      if (res.ok) {
        alert("Activity saved successfully");
        setActivityModalOpen(false);
        setActivityName("");
        setActivityDescription("");
        setElapsedSeconds(0);
      } else {
        alert("Failed to save activity");
      }
    } catch {
      alert("Error saving activity");
    }
  }

  function handleCancelActivity() {
    setActivityModalOpen(false);
    setElapsedSeconds(0);
  }

  function formatTime(seconds: number) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return `${String(h).padStart(2, "0")}:${String(m).padStart(
      2,
      "0"
    )}:${String(s).padStart(2, "0")}`;
  }

  return (
    <div className="basemap-container">
      <div id="mapdiv" className="map-fullscreen" />

      <MapDrawer
        setRouteGeometry={setRouteGeometry}
        clearRoute={() => setRouteGeometry(null)}
        setRouteInstructions={setRouteInstructions}
        setWaterPoints={setWaterPoints}
        setRouteMeta={handleSetRouteMeta}
      />

      <RouteInstructionsList routeInstructions={routeInstructions} />

      {/* BOTTOM-RIGHT BUTTONS */}
      {routeInstructions.length > 0 && (
        <div className="bottom-right-buttons">
          <button onClick={openRouteModal} className="save-button">
            Save Route
          </button>
          <button onClick={handleEndActivity} className="end-button">
            Cancel
          </button>
        </div>
      )}

      {/* BOTTOM-LEFT BUTTONS */}
      {!activityStarted && (
        <div className="bottom-left-buttons">
          <button
            onClick={handleStartActivity}
            className="start-activity-button"
          >
            Start Activity
          </button>
        </div>
      )}
      {activityStarted && (
        <div className="bottom-left-buttons">
          <div className="activity-timer">
            Time: {formatTime(elapsedSeconds)}
          </div>
          <button
            onClick={handleStopActivity}
            className="cancel-activity-button"
          >
            End Activity
          </button>
        </div>
      )}

      {/* SAVE ROUTE MODAL */}
      {routeModalOpen && (
        <div className="modal-overlay">
          <div className="modal-box">
            <h3>Route Name</h3>
            <div className="modal-input-box">
              <input
                type="text"
                className="modal-input"
                placeholder="Your route name"
                value={routeName}
                onChange={(e) => setRouteName(e.target.value)}
              />
            </div>

            <h3>Notes</h3>
            <div className="modal-textarea-box">
              <textarea
                className="modal-textarea"
                placeholder="Notes about your route"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
            </div>

            <div className="modal-buttons">
              <button onClick={handleSaveRoute} className="confirm-button">
                Confirm Save
              </button>
              <button
                onClick={() => setRouteModalOpen(false)}
                className="cancel-button"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* SAVE ACTIVITY MODAL */}
      {activityModalOpen && (
        <div className="modal-overlay">
          <div className="modal-box">
            <h3>Activity Name</h3>
            <div className="modal-input-box">
              <input
                type="text"
                className="modal-input"
                placeholder="Your activity name"
                value={activityName}
                onChange={(e) => setActivityName(e.target.value)}
              />
            </div>

            <h3>Description</h3>
            <div className="modal-textarea-box">
              <textarea
                className="modal-textarea"
                placeholder="Describe your activity"
                value={activityDescription}
                onChange={(e) => setActivityDescription(e.target.value)}
              />
            </div>

            <div className="modal-buttons">
              <button
                onClick={handleConfirmActivity}
                className="confirm-button"
              >
                Confirm Save
              </button>
              <button onClick={handleCancelActivity} className="cancel-button">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <Navigate />
    </div>
  );
}

export default BaseMap;
