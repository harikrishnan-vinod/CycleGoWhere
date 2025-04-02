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
}

const WaterPointsLayer: React.FC<WaterPointsLayerProps> = ({
  map,
  waterPoints,
}) => {
  useEffect(() => {
    if (!map) return;

    waterPoints.forEach((wp) => {
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
    });
  }, [map, waterPoints]);

  return null;
};

export default WaterPointsLayer;
