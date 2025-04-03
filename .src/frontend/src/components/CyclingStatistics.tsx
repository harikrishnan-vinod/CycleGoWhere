import React, { useState, useEffect, useRef } from "react";
import "../components-css/CyclingStatistics.css";

const CyclingStatistics: React.FC = () => {
    const [dates, setDates] = useState<string[]>([]);
    const [selectedDate, setSelectedDate] = useState<string>("");
    const [todayStats, setTodayStats] = useState({ distance: 0, time: 0 });
    const [weekStats, setWeekStats] = useState({ distance: 0, time: 0 });
    const [monthStats, setMonthStats] = useState({ distance: 0, time: 0 });
    const [totalTime, setTotalTime] = useState(0);
    const [rideCount, setRideCount] = useState(0);

    const dateBarRef = useRef<HTMLDivElement>(null);
    const userUID = sessionStorage.getItem("userUID");

    useEffect(() => {
        const today = new Date();
        const startDate = new Date(today.getFullYear(), 0, 1); // Start from January 1st of the current year
        const endDate = new Date(today.getFullYear(), 11, 31); // End at December 31st of the current year

        const dateList: string[] = [];
        let currentDate = new Date(startDate);

        while (currentDate <= endDate) {
            dateList.push(currentDate.toLocaleDateString("en-US", {
                weekday: "short",
                month: "short",
                day: "numeric"
            }));
            currentDate.setDate(currentDate.getDate() + 1);
        }

        setDates(dateList);
        setSelectedDate(today.toLocaleDateString("en-US", {
            weekday: "short",
            month: "short",
            day: "numeric"
        }));
    }, []);
    useEffect(() => {
        if (!selectedDate) return;

        fetch(`/get-activities?userUID=${userUID}`)
            .then((res) => res.json())
            .then((data) => {
                const activities = data.map((activity: any) => ({
                    ...activity,
                    date: new Date(activity.timestamp.seconds * 1000),
                }));

                computeStatistics(activities);
            })
            .catch((err) => console.error("Error fetching activities:", err));
    }, [selectedDate]);

    useEffect(() => {
        const todayString = new Date().toLocaleDateString("en-US", {
            weekday: "short",
            month: "short",
            day: "numeric"
        });

        const dateBar = dateBarRef.current;
        if (dateBar) {
            const todayElement = Array.from(dateBar.getElementsByClassName("date-item")).find(
                (item: any) => item.textContent.trim() === todayString.trim()
            );
            if (todayElement) {
                todayElement.scrollIntoView({ behavior: "smooth" });
            }
        }
    }, [dates]);

    const computeStatistics = (activities: any[]) => {
        const selected = new Date(selectedDate);
        const startOfWeek = new Date(selected);
        startOfWeek.setDate(selected.getDate() - selected.getDay());

        const startOfMonth = new Date(selected.getFullYear(), selected.getMonth(), 1);

        let todayDistance = 0, todayTime = 0;
        let weekDistance = 0, weekTime = 0;
        let monthDistance = 0, monthTime = 0;
        let totalTimeSum = 0;
        let totalRides = activities.length;

        activities.forEach((activity) => {
            const actDate = new Date(activity.timestamp.seconds * 1000);
            const distance = activity.distance || 0;
            const time = activity.duration || 0;

            totalTimeSum += time;

            if (actDate.toISOString().split("T")[0] === selectedDate) {
                todayDistance += distance;
                todayTime += time;
            }

            if (actDate >= startOfWeek && actDate <= selected) {
                weekDistance += distance;
                weekTime += time;
            }

            if (actDate >= startOfMonth && actDate <= selected) {
                monthDistance += distance;
                monthTime += time;
            }
        });

        setTodayStats({ distance: todayDistance, time: todayTime });
        setWeekStats({ distance: weekDistance, time: weekTime });
        setMonthStats({ distance: monthDistance, time: monthTime });
        setTotalTime(totalTimeSum);
        setRideCount(totalRides);
    };

    return (
        <div className="cycling-statistics">
            <div className="date-bar-wrapper">
                <div className="date-bar-container" ref={dateBarRef}>
                    <div className="date-bar">
                        {dates.map((date, index) => {
                            const todayString = new Date().toLocaleDateString("en-US", {
                                weekday: "short",
                                month: "short",
                                day: "numeric"
                            });

                            const isSelected = date === selectedDate;
                            const isToday = date.trim() === todayString.trim();

                            return (
                                <div
                                    key={index}
                                    className={`date-item ${isSelected ? "selected" : ""} ${isToday ? "today" : ""}`}
                                    onClick={() => setSelectedDate(date)}
                                >
                                    {date}
                                </div>
                            );
                        })}
                    </div>                              </div>
            </div>

            <div className="statistics">
                <h3>Statistics for {selectedDate}</h3>
                <p><strong>Today:</strong> {todayStats.distance} km, {todayStats.time} mins</p>
                <p><strong>This Week:</strong> {weekStats.distance} km, {weekStats.time} mins</p>
                <p><strong>This Month:</strong> {monthStats.distance} km, {monthStats.time} mins</p>
                <p><strong>Total Time:</strong> {totalTime} mins</p>
                <p><strong>Number of Rides:</strong> {rideCount}</p>
            </div>
        </div>
    );
};

export default CyclingStatistics;
