//for hooks etc
import { useEffect, useRef, useState } from "react";
import L from "leaflet";
import MapDrawer from "./MapDrawer";
import polyline from "@mapbox/polyline";
import "leaflet-routing-machine";

//for css
import "../../components.css/MapComponents/BaseMap.css";
import "leaflet-routing-machine/dist/leaflet-routing-machine.css";
import "leaflet/dist/leaflet.css";

export default function BaseMap() {
  const mapRef = useRef<L.Map | null>(null);
  const routingControlRef = useRef<L.Routing.Control | null>(null);
  const [routeGeometry, setRouteGeometry] = useState<string | null>(null);

  useEffect(() => {
    if (mapRef.current) return;

    const sw = L.latLng(1.144, 103.535);
    const ne = L.latLng(1.494, 104.502);
    const bounds = L.latLngBounds(sw, ne);

    const map = L.map("mapdiv", {
      center: L.latLng(1.2868108, 103.8545349),
      zoom: 16,
    });

    map.setMaxBounds(bounds);

    L.tileLayer(
      "https://www.onemap.gov.sg/maps/tiles/Default/{z}/{x}/{y}.png",
      {
        detectRetina: true,
        maxZoom: 19,
        minZoom: 11,
        attribution:
          '<img src="https://www.onemap.gov.sg/web-assets/images/logo/om_logo.png" style="height:20px;width:20px;"/>&nbsp;<a href="https://www.onemap.gov.sg/" target="_blank" rel="noopener noreferrer">OneMap</a>&nbsp;&copy;&nbsp;contributors&nbsp;&#124;&nbsp;<a href="https://www.sla.gov.sg/" target="_blank" rel="noopener noreferrer">Singapore Land Authority</a>',
      }
    ).addTo(map);

    mapRef.current = map;
  }, []);

  useEffect(() => {
    if (!mapRef.current || !routeGeometry) return;

    const latlngs = polyline
      .decode(routeGeometry, 5)
      .map(([lat, lng]) => L.latLng(lat, lng));

    // Remove old route if exists
    if (routingControlRef.current) {
      routingControlRef.current.remove();
    }

    // ✅ Custom router to bypass LRM's built-in routing logic
    //@ts-ignore
    const CustomRouter = L.Routing.Router.extend({
      route: function (
        _waypoints: L.Routing.Waypoint[],
        callback: (err: Error | null, routes?: L.Routing.IRoute[]) => void
      ) {
        callback(null, [
          {
            name: "Precomputed Route",
            coordinates: latlngs,
            instructions: [],
            summary: {
              totalDistance: 0,
              totalTime: 0,
            },
            inputWaypoints: [
              L.Routing.waypoint(latlngs[0]),
              L.Routing.waypoint(latlngs[latlngs.length - 1]),
            ],
            actualWaypoints: [latlngs[0], latlngs[latlngs.length - 1]],
          } as any,
        ]);
      },
    });

    // ✅ Plug it into LRM
    routingControlRef.current = L.Routing.control({
      waypoints: [latlngs[0], latlngs[latlngs.length - 1]],
      router: new CustomRouter(),
      fitSelectedRoutes: true,
      show: false,
      addWaypoints: false,
      routeWhileDragging: false,
      //@ts-ignore
      draggableWaypoints: false,
      plan: L.Routing.plan(
        [latlngs[0], latlngs[latlngs.length - 1]].map((pt) =>
          L.Routing.waypoint(pt)
        ),
        {
          createMarker: () => false, // optional: don't show markers
        }
      ),
    }).addTo(mapRef.current);
  }, [routeGeometry]);

  return (
    <>
      <div
        id="mapdiv"
        style={{
          height: "100vh",
          width: "100%",
        }}
      ></div>

      <MapDrawer setRouteGeometry={setRouteGeometry} />
    </>
  );
}
