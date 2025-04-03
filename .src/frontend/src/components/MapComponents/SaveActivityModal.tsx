import React from "react";

export interface SaveActivityModalProps {
  activityName: string;
  activityDescription: string;
  onConfirm: () => void;
  onCancel: () => void;
  onChangeActivityName: React.Dispatch<React.SetStateAction<string>>;
  onChangeActivityDescription: React.Dispatch<React.SetStateAction<string>>;
}

function SaveActivityModal({
  activityName,
  activityDescription,
  onConfirm,
  onCancel,
  onChangeActivityName,
  onChangeActivityDescription,
}: SaveActivityModalProps) {
  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>Activity Name</h3>
        <div className="modal-input-box">
          <input
            type="text"
            className="modal-input"
            placeholder="Your activity name"
            value={activityName}
            onChange={(e) => onChangeActivityName(e.target.value)}
          />
        </div>

        <h3>Description</h3>
        <div className="modal-textarea-box">
          <textarea
            className="modal-textarea"
            placeholder="Describe your activity"
            value={activityDescription}
            onChange={(e) => onChangeActivityDescription(e.target.value)}
          />
        </div>

        <div className="modal-buttons">
          <button onClick={onConfirm} className="confirm-button">
            Confirm Save
          </button>
          <button onClick={onCancel} className="cancel-button">
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default SaveActivityModal;
