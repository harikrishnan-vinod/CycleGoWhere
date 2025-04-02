import React from "react";

interface TimerControlsProps {
  activityStarted: boolean;
  elapsedSeconds: number;
  onStart: () => void;
  onStop: () => void;
}

const formatTime = (seconds: number): string => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(
    s
  ).padStart(2, "0")}`;
};

const TimerControls: React.FC<TimerControlsProps> = ({
  activityStarted,
  elapsedSeconds,
  onStart,
  onStop,
}) => {
  return (
    <div className="bottom-left-buttons">
      {!activityStarted ? (
        <button onClick={onStart} className="start-activity-button">
          Start Activity
        </button>
      ) : (
        <>
          <div className="activity-timer">
            Time: {formatTime(elapsedSeconds)}
          </div>
          <button onClick={onStop} className="cancel-activity-button">
            End Activity
          </button>
        </>
      )}
    </div>
  );
};

export default TimerControls;
