import React, { useState, useRef, useEffect } from "react";
import "../components-css/CyclingStatistics.css";

const CyclingStatistics: React.FC = () => {
    const dateBarRef = useRef<HTMLDivElement>(null);

    const [dates] = useState(() => {
        const startDate = new Date("2025-01-01");
        const today = new Date();
        const endDate = new Date(today);
        endDate.setDate(today.getDate() + 365);

        const dateList: string[] = [];
        let currentDate = new Date(startDate);

        while (currentDate <= endDate) {
            dateList.push(currentDate.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" }));
            currentDate.setDate(currentDate.getDate() + 1);
        }
        return dateList;
    });

    const todayFormatted = new Date().toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
    const todayIndex = dates.findIndex(date => date === todayFormatted);

    useEffect(() => {
        if (dateBarRef.current && todayIndex !== -1) {
            const scrollAmount = todayIndex * 120;
            dateBarRef.current.scrollTo({
                left: scrollAmount,
            });
        }
    }, [todayIndex]);

    return (
        <div className="date-bar-wrapper">
            <div className="date-bar-container" ref={dateBarRef}>
                <div className="date-bar">
                    {dates.map((date, index) => (
                        <div
                            key={index}
                            className={`date-item ${index === todayIndex ? "today" : ""}`}
                        >
                            {date}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default CyclingStatistics;
