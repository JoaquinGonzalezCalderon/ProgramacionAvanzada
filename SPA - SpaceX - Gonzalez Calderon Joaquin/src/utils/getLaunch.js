// src/utils/getLaunch.js
const API = 'https://api.spacexdata.com/v5/launches';

const getLaunch = async (id) => {
    const url = id ? `${API}/${id}` : API;
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`Error HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error('Fetch error:', err);
        return id ? null : [];
    }
};

export default getLaunch;
