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
  markersRef: React.MutableRefObject<L.Marker[]>;
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
        icon: WaterIcon,
      }).addTo(map);
      marker.bindPopup(`<b>${wp.name}</b><br/>Distance: ${wp.distance_km} km`);
      return marker;
    });

    markersRef.current = newMarkers;
  }, [map, waterPoints]);

  return null;
};

export default WaterPointsLayer;
