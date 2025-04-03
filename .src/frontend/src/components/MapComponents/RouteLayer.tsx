import React, { useEffect, useRef } from "react";
import L from "leaflet";
import polyline from "@mapbox/polyline";

interface RouteLayerProps {
  routeGeometry: string | null;
  map: L.Map | null;
}

const RouteLayer: React.FC<RouteLayerProps> = ({ routeGeometry, map }) => {
  const polylineLayerRef = useRef<L.Polyline | null>(null);
  const startMarkerRef = useRef<L.Marker | null>(null);
  const endMarkerRef = useRef<L.Marker | null>(null);

  useEffect(() => {
    // Always clean up old layers
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

    // If no routeGeometry, do nothing else
    if (!map || !routeGeometry) return;

    // Decode polyline and add layers
    const latlngs = polyline
      .decode(routeGeometry, 5)
      .map(([lat, lng]) => L.latLng(lat, lng));

    const newPolyline = L.polyline(latlngs, { color: "blue", weight: 5 }).addTo(
      map
    );
    polylineLayerRef.current = newPolyline;

    const startMarker = L.marker(latlngs[0], { title: "Start" }).addTo(map);
    startMarker.bindPopup("Start").openPopup();
    startMarkerRef.current = startMarker;

    const endMarker = L.marker(latlngs[latlngs.length - 1], {
      title: "Destination",
    }).addTo(map);
    endMarker.bindPopup("Destination");
    endMarkerRef.current = endMarker;

    map.fitBounds(newPolyline.getBounds());
  }, [routeGeometry, map]);

  return null;
};

export default RouteLayer;
