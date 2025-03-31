import "../components-css/personalBest.css";

function PersonalBest() {
    return (
        <div className="pb-page">
            <div className="pb-container">
                <ul className="pb-list">
                    <div className="pb-time">
                        <h3>Fastest: </h3>
                    </div>
                    <div className="pb-distance">
                        <h3>Longest:</h3>
                    </div>

                </ul>
            </div>
        </div>
    )
}

export default PersonalBest;