import React, { useState } from "react";
import { getReport } from "../services/api";

export default function GetReport() {
    const [classNumber, setClassNumber] = useState("");
    const [date, setDate] = useState("");

    const isValidDate = (d) => {
        return /^\d{4}-\d{2}-\d{2}$/.test(d);
    };

    const handleSubmit = async () => {
        const cls = classNumber.trim();
        const dt = date.trim();

        if (!cls || !dt) {
            alert("All fields required");
            return;
        }

        if (!isValidDate(dt)) {
            alert("Date must be in yyyy-mm-dd format");
            return;
        }

        const res = await getReport({
            class_number: cls,
            date: dt,
        });

        // 🔴 handle backend errors
        if (!res.ok) {
            const err = await res.json();
            alert(err.error);
            return;
        }

        // 🔹 download file
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = `report_${cls}_${dt}.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();

        // 🔴 cleanup
        window.URL.revokeObjectURL(url);
    };

    return (
        <div>
            <h3>Download Attendance Report</h3>

            <input
                placeholder="Class Number (e.g., AP2025269049301)"
                onChange={e => setClassNumber(e.target.value)}
            />

            <input
                placeholder="Date (yyyy-mm-dd)"
                onChange={e => setDate(e.target.value)}
            />

            <button onClick={handleSubmit}>Download</button>
        </div>
    );
}