import { useEffect } from "react";
import L from "leaflet";
import "../../components.css/MapComponents/BaseMap.css";
import MapDrawer from "./MapDrawer";

export default function BaseMap() {
  useEffect(() => {
    const script = document.createElement("script");
    script.src =
      "https://www.onemap.gov.sg/web-assets/libs/leaflet/onemap-leaflet.js";
    script.onload = () => {
      const sw = L.latLng(1.144, 103.535);
      const ne = L.latLng(1.494, 104.502);
      const bounds = L.latLngBounds(sw, ne);

      const map = L.map("mapdiv", {
        center: L.latLng(1.2868108, 103.8545349),
        zoom: 16,
      });

      map.setMaxBounds(bounds);

      const basemap = L.tileLayer(
        "https://www.onemap.gov.sg/maps/tiles/Default/{z}/{x}/{y}.png",
        {
          detectRetina: true,
          maxZoom: 19,
          minZoom: 11,
          attribution:
            '<img src="https://www.onemap.gov.sg/web-assets/images/logo/om_logo.png" style="height:20px;width:20px;"/>&nbsp;<a href="https://www.onemap.gov.sg/" target="_blank" rel="noopener noreferrer">OneMap</a>&nbsp;&copy;&nbsp;contributors&nbsp;&#124;&nbsp;<a href="https://www.sla.gov.sg/" target="_blank" rel="noopener noreferrer">Singapore Land Authority</a>',
        }
      );

      basemap.addTo(map);
    };

    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <>
      <link
        rel="stylesheet"
        href="https://www.onemap.gov.sg/web-assets/libs/leaflet/leaflet.css"
      />
      <div id="mapdiv"></div>
      <MapDrawer />
    </>
  );
}
