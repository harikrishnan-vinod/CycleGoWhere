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
  showRepair: boolean;
}

const RepairIcon = L.icon({
  iconUrl: RepairPointIcon,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const RepairPointsLayer: React.FC<RepairPointsLayerProps> = ({
  map,
  RepairPoints,
  markersRef,
  showRepair,
}) => {
  useEffect(() => {
    if (!map) return;

    // Always clear previous markers first
    markersRef.current.forEach((marker) => {
      map.removeLayer(marker);
    });
    markersRef.current = [];

    if (showRepair) {
      const newMarkers = RepairPoints.map((rp) => {
        const marker = L.marker([rp.lat, rp.lng], {
          title: rp.name,
          icon: RepairIcon,
        }).addTo(map);
        marker.bindPopup(
          `<b>${rp.name}</b><br/>Distance: ${rp.distance_km} km`
        );
        return marker;
      });

      markersRef.current = newMarkers;
    }

    return () => {
      markersRef.current.forEach((marker) => {
        map.removeLayer(marker);
      });
      markersRef.current = [];
    };
  }, [map, RepairPoints, showRepair]);

  return null;
};

export default RepairPointsLayer;
