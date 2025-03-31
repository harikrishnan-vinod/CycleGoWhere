import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-routing-machine";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import polyline from "@mapbox/polyline";
import RouteInstructionList from "./RouteInstructionsList";

import "../../components.css/MapComponents/BaseMap.css";
import MapDrawer from "./MapDrawer";

export default function BaseMap() {
  const mapRef = useRef<L.Map | null>(null);
  const startMarkerRef = useRef<L.Marker | null>(null);
  const endMarkerRef = useRef<L.Marker | null>(null);
  const polylineLayerRef = useRef<L.Polyline | null>(null);
  const [routeGeometry, setRouteGeometry] = useState<string | null>(null);
  const [routeInstructions, setRouteInstructions] = useState<any[]>([]);
  const [waterPoints, setWaterPoints] = useState<any[]>([]);
  const waterPointMarkersRef = useRef<L.Marker[]>([]);

  // Initialize the map
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

  // Render route when geometry updates
  useEffect(() => {
    if (!mapRef.current || !routeGeometry) return;

    // Decode the polyline with appropriate precision
    const latlngs = polyline
      .decode(routeGeometry, 5) // set to precision 5 if not the program bricks
      .map(([lat, lng]) => L.latLng(lat, lng));

    // Clear the previous polyline if exists
    if (polylineLayerRef.current) {
      polylineLayerRef.current.remove();
    }
    if (startMarkerRef.current) {
      startMarkerRef.current.remove();
      startMarkerRef.current = null;
    }
    if (endMarkerRef.current) {
      endMarkerRef.current.remove();
      endMarkerRef.current = null;
    }

    // Create a new polyline for the new route
    const polylineLayer = L.polyline(latlngs, {
      color: "blue",
      weight: 5,
    }).addTo(mapRef.current);

    // Store the reference to the polyline
    polylineLayerRef.current = polylineLayer;

    //add start marker to map
    const startMarker = L.marker(latlngs[0], {
      title: "Start",
    }).addTo(mapRef.current);
    startMarker.bindPopup("Start").openPopup();
    startMarkerRef.current = startMarker;

    // add end marker to map
    const endMarker = L.marker(latlngs[latlngs.length - 1], {
      title: "Destination",
    }).addTo(mapRef.current);
    endMarker.bindPopup("Destination");
    endMarkerRef.current = endMarker;

    // Fit map bounds to the route
    mapRef.current.fitBounds(polylineLayer.getBounds());
  }, [routeGeometry]);

  const clearRoute = () => {
    setRouteGeometry(null); // Clear the route geometry state

    // Remove the polyline from the map
    if (polylineLayerRef.current) {
      polylineLayerRef.current.remove(); // Remove the polyline layer
      polylineLayerRef.current = null; // Reset the reference
    }
  };

  useEffect(() => {
    if (!mapRef.current) return;

    // Remove existing waterpoint markers
    waterPointMarkersRef.current.forEach((marker) =>
      mapRef.current!.removeLayer(marker)
    );
    waterPointMarkersRef.current = [];

    if (!waterPoints || waterPoints.length === 0) return;

    const markers: L.Marker[] = waterPoints.map((point) => {
      const marker = L.marker([point.lat, point.lng], {
        title: point.name,
        icon: L.icon({
          iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
          iconSize: [25, 25],
          iconAnchor: [12, 24],
          popupAnchor: [0, -20],
        }),
      }).addTo(mapRef.current!);

      marker.bindPopup(`
        <b>${point.name}</b><br/>
        Distance: ${point.distance_km} km
      `);

      return marker;
    });

    // Save references to clean up later
    waterPointMarkersRef.current = markers;
  }, [waterPoints]);

  return (
    <>
      <div
        id="mapdiv"
        style={{
          height: "100vh",
          width: "100%",
        }}
      ></div>

      <MapDrawer
        setRouteGeometry={setRouteGeometry}
        clearRoute={clearRoute}
        setRouteInstructions={setRouteInstructions}
        setWaterPoints={setWaterPoints}
      />
      <RouteInstructionList routeInstructions={routeInstructions} />
    </>
  );
}
