import '../components-css/savedActivity.css';

function SavedActivity() {
    return (
        <div className="saved-activity-container">
            <div className="saved-activity-top">
                <div className="saved-activity-title">
                    <h2> Title </h2>
                </div>

                <div className="saved-activity-description">
                    Description
                </div>
                <div className="saved-activity-last-used">
                    <p>Last Used</p>
                </div>

            </div>
            <div className="saved-activity-map">

            </div>
            <div className="saved-activity-details">
                <div className="saved-activity-distance">
                    <p>Distance</p>
                </div>
                <div>
                    <button className="start-activity-from-route-btn">
                        Start Activity
                    </button>
                </div>

            </div>

        </div>
    )
}

export default SavedActivity;