import React, { useState } from "react";
import { createClass } from "../services/api";

export default function CreateClass() {
    const [data, setData] = useState({
        class_code: "",
        class_name: "",
        class_number: "",
        slot: "",
        type: "",
        semester: "",
        year: "",
        capacity: ""
    });

    const handleSubmit = async () => {
        // 🔴 required fields
        if (!data.class_code || !data.class_name || !data.class_number) {
            alert("Class Code, Name and Class Number are required");
            return;
        }

        if (!data.slot) {
            alert("Slot is required (e.g., A1, B2)");
            return;
        }

        if (!data.type) {
            alert("Please select class type (Theory/Lab)");
            return;
        }

        if (!data.semester) {
            alert("Semester is required");
            return;
        }

        if (!data.year || isNaN(data.year)) {
            alert("Year must be a number");
            return;
        }

        if (!data.capacity || isNaN(data.capacity) || data.capacity <= 0) {
            alert("Capacity must be a positive number");
            return;
        }

        const res = await createClass({
            ...data,
            year: Number(data.year),
            capacity: Number(data.capacity)
        });

        alert(JSON.stringify(res));
    };

    return (
        <div>
            <h3>Create Class</h3>

            <input
                placeholder="Class Code (e.g., CSE4002)"
                onChange={e => setData({ ...data, class_code: e.target.value.trim() })}
            />

            <input
                placeholder="Class Name"
                onChange={e => setData({ ...data, class_name: e.target.value.trim() })}
            />

            <input
                placeholder="Class Number (unique)"
                onChange={e => setData({ ...data, class_number: e.target.value.trim() })}
            />

            <input
                placeholder="Slot (A1, B2)"
                onChange={e => setData({ ...data, slot: e.target.value.trim() })}
            />

            <select
                onChange={e => setData({ ...data, type: e.target.value })}
            >
                <option value="">Select Type</option>
                <option value="theory">Theory</option>
                <option value="lab">Lab</option>
            </select>

            <input
                placeholder="Semester (e.g., fallsem_2026)"
                onChange={e => setData({ ...data, semester: e.target.value.trim() })}
            />

            <input
                placeholder="Year (e.g., 2026)"
                type="number"
                onChange={e => setData({ ...data, year: e.target.value })}
            />

            <input
                placeholder="Capacity (e.g., 60)"
                type="number"
                onChange={e => setData({ ...data, capacity: e.target.value })}
            />

            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}