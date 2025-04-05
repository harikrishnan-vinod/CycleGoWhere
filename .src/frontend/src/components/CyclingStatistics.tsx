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
    const [weekRange, setWeekRange] = useState<string>("");

    const userUID = sessionStorage.getItem("userUID");
    const dateBarRef = useRef<HTMLDivElement>(null);

    const toLocalDateString = (date: Date) =>
        date.toLocaleDateString("sv-SE"); // "YYYY-MM-DD" in local timezone

    useEffect(() => {
        const today = new Date();
        const yearStart = new Date(today.getFullYear(), 0, 1);
        const yearEnd = new Date(today.getFullYear(), 11, 31);
        const dateList: string[] = [];
        let currentDate = new Date(yearStart);

        while (currentDate <= yearEnd) {
            dateList.push(toLocalDateString(currentDate));
            currentDate.setDate(currentDate.getDate() + 1);
        }

        setDates(dateList);

        const todayString = toLocalDateString(today);
        setSelectedDate(todayString);
        setWeekRangeForDate(today);

        setTimeout(() => {
            const todayElement = document.querySelector(`[data-date='${todayString}']`);
            if (todayElement) {
                todayElement.scrollIntoView({ behavior: "smooth", inline: "center" });
            }
        }, 100);
    }, []);

    useEffect(() => {
        if (!selectedDate) return;

        fetch(`http://localhost:1234/get-activities?userUID=${userUID}`)
            .then(async (res) => {
                if (!res.ok) {
                    throw new Error(`HTTP error! Status: ${res.status}`);
                }

                const contentType = res.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    const text = await res.text();
                    console.error("Non-JSON response body:", text);
                    throw new Error("Received non-JSON response from the server");
                }

                return res.json();
            })
            .then((data) => {
                computeStatistics(data);
            })
            .catch((err) => console.error("Error fetching activities:", err.message));
    }, [selectedDate]);

    const computeStatistics = (activities: any[]) => {
        const selected = new Date(selectedDate);
        selected.setHours(0, 0, 0, 0);

        const startOfWeek = new Date(selected);
        startOfWeek.setDate(selected.getDate() - selected.getDay()); // Sunday is the first day of the week (fixed)
        startOfWeek.setHours(0, 0, 0, 0);

        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6);
        endOfWeek.setHours(23, 59, 59, 999);

        const startOfMonth = new Date(selected.getFullYear(), selected.getMonth(), 1);
        startOfMonth.setHours(0, 0, 0, 0);

        let todayDistance = 0, todayTime = 0;
        let weekDistance = 0, weekTime = 0;
        let monthDistance = 0, monthTime = 0;
        let totalTimeSum = 0;
        let totalRides = activities.length;

        activities.forEach((activity) => {
            const actDate = new Date(activity.createdAt);
            actDate.setHours(0, 0, 0, 0);
            const distance = activity.distance || 0;
            const time = activity.duration || 0;

            totalTimeSum += time;

            // Today
            if (actDate.getTime() === selected.getTime()) {
                todayDistance += distance;
                todayTime += time;
            }

            // Week
            if (actDate >= startOfWeek && actDate <= endOfWeek) {
                weekDistance += distance;
                weekTime += time;
            }

            // Month
            if (
                actDate.getFullYear() === selected.getFullYear() &&
                actDate.getMonth() === selected.getMonth()
            ) {
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


    const setWeekRangeForDate = (date: Date) => {
        const startOfWeek = new Date(date);
        startOfWeek.setDate(date.getDate() - date.getDay());
        const endOfWeek = new Date(startOfWeek);
        endOfWeek.setDate(startOfWeek.getDate() + 6);

        const formattedStart = startOfWeek.toLocaleDateString("en-GB", { day: "numeric", month: "short" });
        const formattedEnd = endOfWeek.toLocaleDateString("en-GB", { day: "numeric", month: "short" });

        setWeekRange(`${formattedStart} - ${formattedEnd}`);
    };

    return (
        <div className="cycling-statistics">
            <div className="week-range">
                <h4>{weekRange}</h4>
            </div>

            <div className="date-bar" ref={dateBarRef}>
                {dates.map((date, index) => (
                    <div
                        key={index}
                        className={`date-item ${date === selectedDate ? "selected" : ""}`}
                        data-date={date}
                        onClick={() => {
                            setSelectedDate(date);
                            setWeekRangeForDate(new Date(date));
                        }}
                    >
                        {new Date(date).toLocaleDateString("en-US", {
                            month: "short",
                            day: "numeric"
                        })}
                    </div>
                ))}
            </div>

            <div className="statistics">
                <h3>
                    Statistics for{" "}
                    {new Date(selectedDate).toLocaleDateString("en-US", {
                        month: "long",
                        day: "numeric",
                        year: "numeric"
                    })}
                </h3>
                <p><strong>Today:</strong> {(todayStats.distance / 1000).toFixed(1)} km, {(todayStats.time / 60).toFixed(1)} mins</p>
                <p><strong>This Week:</strong> {(weekStats.distance / 1000).toFixed(1)} km, {(weekStats.time / 60).toFixed(1)} mins</p>
                <p><strong>This Month:</strong> {(monthStats.distance / 1000).toFixed(1)} km, {(monthStats.time / 60).toFixed(1)} mins</p>
                <p><strong>Total Time:</strong> {(totalTime / 60).toFixed(1)} mins</p>
                <p><strong>Number of Rides:</strong> {rideCount}</p>
            </div>
        </div>
    );
};

export default CyclingStatistics;
