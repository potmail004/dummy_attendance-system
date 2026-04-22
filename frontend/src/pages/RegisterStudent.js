import React, { useState } from "react";
import { registerStudent } from "../services/api";

export default function RegisterStudent() {
    const [name, setName] = useState("");
    const [code, setCode] = useState("");
    const [phone, setPhone] = useState("");
    const [year, setYear] = useState("");
    const [files, setFiles] = useState([]);

    const handleSubmit = async () => {
        // 🔴 basic validation
        if (!name || !code) {
            alert("Name and Student ID are required");
            return;
        }

        if (year && isNaN(year)) {
            alert("Year must be a number");
            return;
        }

        const formData = new FormData();
        formData.append("name", name);
        formData.append("student_code", code);
        formData.append("phone", phone || "");
        formData.append("year_of_joining", year ? Number(year) : "");

        for (let f of files) formData.append("files", f);

        const res = await registerStudent(formData);
        alert(JSON.stringify(res));
    };

    return (
        <div>
            <h3>Register Student</h3>

            <input placeholder="Name" onChange={e => setName(e.target.value)} />
            <input placeholder="Student ID" onChange={e => setCode(e.target.value)} />
            <input placeholder="Phone (optional)" onChange={e => setPhone(e.target.value)} />
            <input
                placeholder="Year of Joining"
                type="number"
                onChange={e => setYear(e.target.value)}
            />

            <input type="file" multiple onChange={e => setFiles(e.target.files)} />

            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}