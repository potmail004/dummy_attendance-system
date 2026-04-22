import React, { useState } from "react";
import { registerTeacher } from "../services/api";

export default function RegisterTeacher() {
    const [code, setCode] = useState("");
    const [name, setName] = useState("");

    const handleSubmit = async () => {
        if (!code || !name) {
            alert("All fields required");
            return;
        }

        const res = await registerTeacher({
            teacher_code: code,
            full_name: name
        });

        alert(JSON.stringify(res));
    };

    return (
        <div>
            <h3>Register Teacher</h3>
            <input placeholder="Teacher Code" onChange={e => setCode(e.target.value)} />
            <input placeholder="Name" onChange={e => setName(e.target.value)} />
            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}