import React, { useEffect } from "react";
import L from "leaflet";
import RepairPointIcon from "../../assets/repairshop.png";

interface RepairPoint {
  lat: number;
  lng: number;
  name: string;
  distance_km: number;
}

interface RepairPointsLayerProps {
  map: L.Map | null;
  RepairPoints: RepairPoint[];
  markersRef: React.MutableRefObject<L.Marker[]>;
}

const RepairIcon = L.icon({
  iconUrl: RepairPointIcon, // or iconUrl if from public folder
  iconSize: [32, 32], // size of the icon
  iconAnchor: [16, 32], // point of the icon which will correspond to marker's location
  popupAnchor: [0, -32], // point from which the popup should open relative to the iconAnchor
});

const RepairPointsLayer: React.FC<RepairPointsLayerProps> = ({
  map,
  RepairPoints,
  markersRef,
}) => {
  useEffect(() => {
    if (!map) return;

    // Clear previous markers
    markersRef.current.forEach((marker) => {
      map.removeLayer(marker);
    });
    markersRef.current = [];

    const newMarkers = RepairPoints.map((rp) => {
      const marker = L.marker([rp.lat, rp.lng], {
        title: rp.name,
        icon: RepairIcon,
      }).addTo(map);
      marker.bindPopup(`<b>${rp.name}</b><br/>Distance: ${rp.distance_km} km`);
      return marker;
    });

    markersRef.current = newMarkers;
  }, [map, RepairPoints]);

  return null;
};

export default RepairPointsLayer;
