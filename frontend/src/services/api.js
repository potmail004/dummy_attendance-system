const BASE_URL = "http://127.0.0.1:8000";

export const registerStudent = async (formData) => {
    return fetch(`${BASE_URL}/register/student`, {
        method: "POST",
        body: formData,
    }).then(res => res.json());
};

export const registerTeacher = async (data) => {
    return fetch(`${BASE_URL}/teacher/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    }).then(res => res.json());
};

export const createClass = async (data) => {
    return fetch(`${BASE_URL}/class/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    }).then(res => res.json());
};

export const recognize = async (formData) => {
    return fetch(`${BASE_URL}/recognize`, {
        method: "POST",
        body: formData,
    }).then(res => res.json());
};

export const getReport = async (data) => {
    const res = await fetch(`${BASE_URL}/report`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });

    return res; // ⚠️ return raw response (needed for file)
};