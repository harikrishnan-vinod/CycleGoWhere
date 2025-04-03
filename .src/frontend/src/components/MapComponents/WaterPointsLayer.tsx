import React, { useEffect } from "react";
import L from "leaflet";

interface WaterPoint {
  lat: number;
  lng: number;
  name: string;
  distance_km: number;
}

interface WaterPointsLayerProps {
  map: L.Map | null;
  waterPoints: WaterPoint[];
  markersRef: React.MutableRefObject<L.Marker[]>;
}

const WaterPointsLayer: React.FC<WaterPointsLayerProps> = ({
  map,
  waterPoints,
  markersRef,
}) => {
  useEffect(() => {
    if (!map) return;

    // Clear previous markers
    markersRef.current.forEach((marker) => {
      map.removeLayer(marker);
    });
    markersRef.current = [];

    const newMarkers = waterPoints.map((wp) => {
      const marker = L.marker([wp.lat, wp.lng], {
        title: wp.name,
        icon: L.icon({
          iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
          iconSize: [25, 25],
          iconAnchor: [12, 24],
          popupAnchor: [0, -20],
        }),
      }).addTo(map);
      marker.bindPopup(`<b>${wp.name}</b><br/>Distance: ${wp.distance_km} km`);
      return marker;
    });

    markersRef.current = newMarkers;
  }, [map, waterPoints]);

  return null;
};

export default WaterPointsLayer;
