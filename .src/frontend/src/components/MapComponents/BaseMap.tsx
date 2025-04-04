import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-routing-machine";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import Navigate from "../../components/Navigation";
import MapDrawer from "./MapDrawer";
import RouteInstructionsList from "./RouteInstructionsList";
import RouteLayer from "./RouteLayer";
import WaterPointsLayer from "./WaterPointsLayer";
import TimerControls from "./TimerControls";
import SaveRouteModal from "./SaveRouteModal";
import SaveActivityModal from "./SaveActivityModal";
import "../../components.css/MapComponents/BaseMap.css";
import personIcon from "../../assets/personpositionicon.png";
import { useMemo } from "react";
import { RouteSummary } from "../../types";
import RouteSummaryComponent from "./RouteSummaryComponent";

function BaseMap() {
  // for map
  const mapRef = useRef<L.Map | null>(null);
  const [routeGeometry, setRouteGeometry] = useState<string | null>(null);
  const [waterPoints, setWaterPoints] = useState<any[]>([]);
  const userMarkerRef = useRef<L.Marker | null>(null);

  // for instructions
  const [routeInstructions, setRouteInstructions] = useState<any[]>([]);
  const [currentInstructionIndex, setCurrentInstructionIndex] = useState(0);
  const [routeSummary, setRouteSummary] = useState<RouteSummary | null>(null);

  // for activities
  const [distance, setDistance] = useState<number>(0);
  const [startPostal, setStartPostal] = useState("");
  const [endPostal, setEndPostal] = useState("");
  const [routeModalOpen, setRouteModalOpen] = useState(false);
  const [routeName, setRouteName] = useState("");
  const [notes, setNotes] = useState("");
  const [activityStarted, setActivityStarted] = useState(false);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const [activityModalOpen, setActivityModalOpen] = useState(false);
  const [activityName, setActivityName] = useState("");
  const [activityDescription, setActivityDescription] = useState("");
  const [activityStartTime, setActivityStartTime] = useState<Date | null>(null);

  // declare icons
  const userIcon = L.icon({
    iconUrl: personIcon, // or iconUrl if from public folder
    iconSize: [32, 32], // size of the icon
    iconAnchor: [16, 32], // point of the icon which will correspond to marker's location
    popupAnchor: [0, -32], // point from which the popup should open relative to the iconAnchor
  });

  // mock locations from 637035 to 648310
  const mockLocations = useMemo(() => {
    if (!routeInstructions || routeInstructions.length === 0) return [];

    return routeInstructions.map((instruction) => {
      const [latStr, lngStr] = instruction[3].split(",");
      return {
        lat: parseFloat(latStr),
        lng: parseFloat(lngStr),
      };
    });
  }, [routeInstructions]);

  const locationIndexRef = useRef(0);

  useEffect(() => {
    if (mapRef.current) return;

    const map = L.map("mapdiv", {
      center: L.latLng(1.2868108, 103.8545349), // fallback
      zoom: 16,
    });

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

    // 1. Get initial position
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;

        const marker = L.marker([latitude, longitude], { icon: userIcon })
          .addTo(map)
          .bindPopup("You are here")
          .openPopup();

        userMarkerRef.current = marker;
        map.setView([latitude, longitude], 16);
      },
      (error) => {
        console.error("Initial geolocation error:", error);
        alert("Unable to retrieve your initial location.");
      },
      {
        enableHighAccuracy: true,
        timeout: 5000,
      }
    );
  }, []);

  const updateLocation = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();

    const index = locationIndexRef.current;
    const { lat, lng } = mockLocations[index];

    console.log("📍 Moving to index:", index, "Location:", lat, lng);

    locationIndexRef.current = (index + 1) % mockLocations.length;

    if (mapRef.current) {
      const map = mapRef.current;

      // === Remove previous marker ===
      if (userMarkerRef.current) {
        map.removeLayer(userMarkerRef.current);
        userMarkerRef.current = null; // ✅ Clear reference
      }

      // === Add new marker ===
      const marker = L.marker([lat, lng], { icon: userIcon })
        .addTo(map)
        .bindPopup("You are here")
        .openPopup();

      userMarkerRef.current = marker;
      map.setView([lat, lng], 16);

      // === Proximity check ===
      if (
        routeInstructions.length > 0 &&
        currentInstructionIndex < routeInstructions.length
      ) {
        const currentPos = L.latLng(lat, lng);
        const nextStep = routeInstructions[currentInstructionIndex];
        const [latStr, lngStr] = nextStep[3].split(",");
        const nextPos = L.latLng(parseFloat(latStr), parseFloat(lngStr));

        const distance = currentPos.distanceTo(nextPos);

        if (distance <= 20) {
          console.log(
            `✅ Arrived at waypoint ${currentInstructionIndex}:`,
            nextStep
          );

          setRouteInstructions((prevInstructions) => {
            const updated = prevInstructions.slice(1);
            locationIndexRef.current = 0;

            return updated;
          });

          setCurrentInstructionIndex(0);
        }
      }
    }
  };

  function handleSetRouteMeta(
    dist: number,
    startPost: string,
    endPost: string
  ) {
    setDistance(dist);
    setStartPostal(startPost);
    setEndPostal(endPost);
  }

  function handleStartActivity() {
    if (!activityStarted) {
      setActivityStarted(true);
      setElapsedSeconds(0);
      setActivityStartTime(new Date());
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

  function handleEndActivity() {
    setActivityStarted(false);
    setRouteInstructions([]);
    setRouteGeometry(null);
    setWaterPoints([]);
    setCurrentInstructionIndex(0);
    setRouteSummary(null);
    locationIndexRef.current = 0;

    // Clear map layers except user marker
    if (mapRef.current) {
      const map = mapRef.current;

      map.eachLayer((layer) => {
        // Preserve the base tile layer and user marker only
        const isTileLayer = (layer as any)._url?.includes("onemap.gov.sg");
        const isUserMarker = layer === userMarkerRef.current;

        if (!isTileLayer && !isUserMarker) {
          map.removeLayer(layer);
        }
      });
    }
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
      startTime: activityStartTime?.toISOString(),
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
  return (
    <div className="basemap-container">
      <div id="mapdiv" className="map-fullscreen" />

      <MapDrawer
        setRouteGeometry={setRouteGeometry}
        clearRoute={() => setRouteGeometry(null)}
        setRouteInstructions={setRouteInstructions}
        setWaterPoints={setWaterPoints}
        setRouteMeta={handleSetRouteMeta}
        setRouteSummary={setRouteSummary}
      />
      <div className="route-summarybox">
        <RouteInstructionsList
          routeInstructions={routeInstructions}
          activityStarted={activityStarted}
        />
        <RouteSummaryComponent
          routeSummary={routeSummary}
          activityStarted={activityStarted}
        />
      </div>

      <RouteLayer map={mapRef.current} routeGeometry={routeGeometry} />
      <WaterPointsLayer map={mapRef.current} waterPoints={waterPoints} />

      {activityStarted && (
        <div className="next-location-button">
          <button onClick={updateLocation}>Next Location</button>
        </div>
      )}

      {routeInstructions.length > 0 && (
        <div className="bottom-right-buttons">
          <button
            onClick={() => setRouteModalOpen(true)}
            className="save-button"
          >
            Save Route
          </button>
          <button onClick={handleEndActivity} className="end-button">
            Cancel
          </button>
        </div>
      )}

      {routeInstructions.length > 0 && (
        <TimerControls
          activityStarted={activityStarted}
          elapsedSeconds={elapsedSeconds}
          onStart={handleStartActivity}
          onStop={handleStopActivity}
        />
      )}

      {routeModalOpen && (
        <SaveRouteModal
          routeName={routeName}
          notes={notes}
          onNameChange={setRouteName}
          onNotesChange={setNotes}
          onConfirm={handleSaveRoute}
          onCancel={() => setRouteModalOpen(false)}
        />
      )}

      {routeInstructions.length > 0 && activityModalOpen && (
        <SaveActivityModal
          activityName={activityName}
          activityDescription={activityDescription}
          onConfirm={handleConfirmActivity}
          onCancel={handleCancelActivity}
          onChangeActivityName={setActivityName}
          onChangeActivityDescription={setActivityDescription}
        />
      )}

      <Navigate />
    </div>
  );
}

export default BaseMap;
