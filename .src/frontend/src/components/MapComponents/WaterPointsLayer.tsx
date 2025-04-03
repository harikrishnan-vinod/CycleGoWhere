import React, { useEffect } from "react";
import L from "leaflet";
import WaterPointIcon from "../../assets/water-tap.png";

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

const WaterIcon = L.icon({
  iconUrl: WaterPointIcon, // or iconUrl if from public folder
  iconSize: [32, 32], // size of the icon
  iconAnchor: [16, 32], // point of the icon which will correspond to marker's location
  popupAnchor: [0, -32], // point from which the popup should open relative to the iconAnchor
});

const WaterPointsLayer: React.FC<WaterPointsLayerProps> = ({
  map,
  waterPoints,
}) => {
  useEffect(() => {
    if (!map) return;

    waterPoints.forEach((wp) => {
      const marker = L.marker([wp.lat, wp.lng], { icon: WaterIcon }).addTo(map);

      marker.bindPopup(`<b>${wp.name}</b><br/>Distance: ${wp.distance_km} km`);
    });
  }, [map, waterPoints]);

  return null;
};

export default WaterPointsLayer;
