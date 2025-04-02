import React from "react";

interface SaveRouteModalProps {
  routeName: string;
  notes: string;
  onNameChange: (val: string) => void;
  onNotesChange: (val: string) => void;
  onConfirm: () => void;
  onCancel: () => void;
}

const SaveRouteModal: React.FC<SaveRouteModalProps> = ({
  routeName,
  notes,
  onNameChange,
  onNotesChange,
  onConfirm,
  onCancel,
}) => {
  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>Route Name</h3>
        <div className="modal-input-box">
          <input
            type="text"
            className="modal-input"
            placeholder="Your route name"
            value={routeName}
            onChange={(e) => onNameChange(e.target.value)}
          />
        </div>

        <h3>Notes</h3>
        <div className="modal-textarea-box">
          <textarea
            className="modal-textarea"
            placeholder="Notes about your route"
            value={notes}
            onChange={(e) => onNotesChange(e.target.value)}
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
};

export default SaveRouteModal;
