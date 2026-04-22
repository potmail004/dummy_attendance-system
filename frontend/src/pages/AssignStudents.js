import React, { useState } from "react";

export default function AssignStudents() {
    const [classCode, setClassCode] = useState("");
    const [studentCodes, setStudentCodes] = useState("");

    const handleSubmit = async () => {
        if (!classCode || !studentCodes) {
            alert("Class Code and Student Codes required");
            return;
        }

        // 🔴 keep as strings
        const codes = studentCodes.split(",").map((id) => id.trim());

        const res = await fetch("http://127.0.0.1:8000/class/assign-students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                class_number: classCode,
                student_codes: codes,
            }),
        });

        const data = await res.json();
        alert(JSON.stringify(data));
    };

    return (
        <div>
            <h3>Assign Students to Class</h3>

            <input
                placeholder="Class Number"
                onChange={(e) => setClassCode(e.target.value)}
            />

            <input
                placeholder="Student Codes (comma separated: 22BCE20428,22BCE20429)"
                onChange={(e) => setStudentCodes(e.target.value)}
            />

            <button onClick={handleSubmit}>Assign</button>
        </div>
    );
}