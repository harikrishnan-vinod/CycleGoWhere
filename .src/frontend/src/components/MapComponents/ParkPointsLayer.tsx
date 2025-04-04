import React, { useEffect } from "react";
import L from "leaflet";
import ParkingPointIcon from "../../assets/bikeparking.png";

interface ParkPoint {
  lat: number;
  lng: number;
  name: string;
  distance_km: number;
}

interface ParkPointsLayerProps {
  map: L.Map | null;
  parkPoints: ParkPoint[];
  markersRef: React.MutableRefObject<L.Marker[]>;
}

const ParkingIcon = L.icon({
  iconUrl: ParkingPointIcon, // or iconUrl if from public folder
  iconSize: [32, 32], // size of the icon
  iconAnchor: [16, 32], // point of the icon which will correspond to marker's location
  popupAnchor: [0, -32], // point from which the popup should open relative to the iconAnchor
});

const ParkPointsLayer: React.FC<ParkPointsLayerProps> = ({
  map,
  parkPoints,
  markersRef,
}) => {
  useEffect(() => {
    if (!map) return;

    // Clear previous markers
    markersRef.current.forEach((marker) => {
      map.removeLayer(marker);
    });
    markersRef.current = [];

    const newMarkers = parkPoints.map((pp) => {
      const marker = L.marker([pp.lat, pp.lng], {
        title: pp.name,
        icon: ParkingIcon,
      }).addTo(map);
      marker.bindPopup(`<b>${pp.name}</b><br/>Distance: ${pp.distance_km} km`);
      return marker;
    });

    markersRef.current = newMarkers;
  }, [map, parkPoints]);

  return null;
};

export default ParkPointsLayer;
