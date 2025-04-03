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
    if (!map || !routeGeometry) return;
    const latlngs = polyline
      .decode(routeGeometry, 5)
      .map(([lat, lng]) => L.latLng(lat, lng));

    polylineLayerRef.current?.remove();
    startMarkerRef.current?.remove();
    endMarkerRef.current?.remove();

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
