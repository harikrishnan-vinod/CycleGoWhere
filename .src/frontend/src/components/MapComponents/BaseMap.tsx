import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet-routing-machine";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import polyline from "@mapbox/polyline";

import RouteInstructionsList from "./RouteInstructionsList";
import MapDrawer from "./MapDrawer";
import Navigate from "../../components/Navigation";

import "../../components.css/MapComponents/BaseMap.css";

export default function BaseMap() {
  const mapRef = useRef<L.Map | null>(null);
  const startMarkerRef = useRef<L.Marker | null>(null);
  const endMarkerRef = useRef<L.Marker | null>(null);
  const polylineLayerRef = useRef<L.Polyline | null>(null);

  const [routeGeometry, setRouteGeometry] = useState<string | null>(null);
  const [routeInstructions, setRouteInstructions] = useState<any[]>([]);

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

  useEffect(() => {
    if (!mapRef.current || !routeGeometry) return;

    const latlngs = polyline
      .decode(routeGeometry, 5) // precision
      .map(([lat, lng]) => L.latLng(lat, lng));

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

    const newPolyline = L.polyline(latlngs, {
      color: "blue",
      weight: 5,
    }).addTo(mapRef.current);
    polylineLayerRef.current = newPolyline;

    const startMarker = L.marker(latlngs[0], { title: "Start" }).addTo(
      mapRef.current
    );
    startMarker.bindPopup("Start").openPopup();
    startMarkerRef.current = startMarker;

    const endMarker = L.marker(latlngs[latlngs.length - 1], {
      title: "Destination",
    }).addTo(mapRef.current);
    endMarker.bindPopup("Destination");
    endMarkerRef.current = endMarker;

    mapRef.current.fitBounds(newPolyline.getBounds());
  }, [routeGeometry]);

  const clearRoute = () => {
    setRouteGeometry(null);
    if (polylineLayerRef.current) {
      polylineLayerRef.current.remove();
      polylineLayerRef.current = null;
    }
  };

  return (
    <div className="basemap-container">
      <div id="mapdiv" className="map-fullscreen" />

      <MapDrawer
        setRouteGeometry={setRouteGeometry}
        clearRoute={clearRoute}
        setRouteInstructions={setRouteInstructions}
      />

      <RouteInstructionsList routeInstructions={routeInstructions} />

      <Navigate />
    </div>
  );
}
