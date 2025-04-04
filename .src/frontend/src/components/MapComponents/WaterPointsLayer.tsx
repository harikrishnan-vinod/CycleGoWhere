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
  showWater: boolean;
}

const WaterIcon = L.icon({
  iconUrl: WaterPointIcon,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const WaterPointsLayer: React.FC<WaterPointsLayerProps> = ({
  map,
  waterPoints,
  markersRef,
  showWater,
}) => {
  useEffect(() => {
    if (!map) return;

    // Clear previous markers
    markersRef.current.forEach((marker) => {
      map.removeLayer(marker);
    });
    markersRef.current = [];

    // Add new markers if visible
    if (showWater) {
      const newMarkers = waterPoints.map((wp) => {
        const marker = L.marker([wp.lat, wp.lng], {
          title: wp.name,
          icon: WaterIcon,
        }).addTo(map);
        marker.bindPopup(
          `<b>${wp.name}</b><br/>Distance: ${wp.distance_km} km`
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
  }, [map, waterPoints, showWater]);

  return null;
};

export default WaterPointsLayer;
