import React, { useState } from "react";
import { recognize } from "../services/api";

export default function Recognize() {
    const [classId, setClassId] = useState("");
    const [teacherId, setTeacherId] = useState("");
    const [files, setFiles] = useState([]);

    const handleSubmit = async () => {
        if (!classId || !teacherId) {
            alert("Class ID and Teacher ID required");
            return;
        }

        const formData = new FormData();
        formData.append("class_number", classId);
        formData.append("teacher_code", teacherId);

        for (let f of files) formData.append("files", f);

        const res = await recognize(formData);
        alert(JSON.stringify(res));
    };

    return (
        <div>
            <h3>Recognize Attendance</h3>

            <input placeholder="Class Number" onChange={e => setClassId(e.target.value)} />
            <input placeholder="Teacher ID" onChange={e => setTeacherId(e.target.value)} />

            <input type="file" multiple onChange={e => setFiles(e.target.files)} />

            <button onClick={handleSubmit}>Submit</button>
        </div>
    );
}