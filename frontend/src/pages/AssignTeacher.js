import React, { useState } from "react";

export default function AssignTeacher() {
    const [classId, setClassId] = useState("");
    const [teacherId, setTeacherId] = useState("");

    const handleSubmit = async () => {
        if (!classId || !teacherId) {
            alert("Class ID and Teacher ID required");
            return;
        }

        const res = await fetch("http://127.0.0.1:8000/class/assign-teacher", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                class_number: classId,
                teacher_code: teacherId
            }),
        });

        const data = await res.json();
        alert(JSON.stringify(data));
    };

    return (
        <div>
            <h3>Assign Teacher to Class</h3>

            <input
                placeholder="Class Number"
                onChange={(e) => setClassId(e.target.value)}
            />

            <input
                placeholder="Teacher ID"
                onChange={(e) => setTeacherId(e.target.value)}
            />

            <button onClick={handleSubmit}>Assign</button>
        </div>
    );
}