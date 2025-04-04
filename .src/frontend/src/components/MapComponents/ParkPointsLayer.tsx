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
  showPark: boolean;
}

const ParkingIcon = L.icon({
  iconUrl: ParkingPointIcon,
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

const ParkPointsLayer: React.FC<ParkPointsLayerProps> = ({
  map,
  parkPoints,
  markersRef,
  showPark,
}) => {
  useEffect(() => {
    if (!map) return;

    // Clear previous markers
    markersRef.current.forEach((marker) => {
      map.removeLayer(marker);
    });
    markersRef.current = [];

    // Only add markers if showPark is true
    if (showPark) {
      const newMarkers = parkPoints.map((pp) => {
        const marker = L.marker([pp.lat, pp.lng], {
          title: pp.name,
          icon: ParkingIcon,
        }).addTo(map);
        marker.bindPopup(
          `<b>${pp.name}</b><br/>Distance: ${pp.distance_km} km`
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
  }, [map, parkPoints, showPark]);

  return null;
};

export default ParkPointsLayer;
