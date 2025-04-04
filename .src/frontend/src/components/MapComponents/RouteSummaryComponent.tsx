import { RouteSummary } from "../../types";
import "../../components.css/MapComponents/RouteSummaryComponent.css";

interface RouteSummaryComponentProps {
  routeSummary: RouteSummary | null;
  activityStarted: boolean;
}

function RouteSummaryComponent({
  routeSummary,
  activityStarted,
}: RouteSummaryComponentProps) {
  if (activityStarted) return null;
  if (routeSummary === null) return null;

  return (
    <div className="route-summary-box">
      <h4>Route Summary</h4>
      <div>
        <strong>Distance:</strong>{" "}
        {(routeSummary.total_distance / 1000).toFixed(2)} km
      </div>
      <div>
        <strong>Estimated Time:</strong>{" "}
        {(routeSummary.total_time / 60).toFixed(0)} min
      </div>
    </div>
  );
}

export default RouteSummaryComponent;
