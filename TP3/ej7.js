function wordFreq(text) {
    const map = new Map();
    if (!text) return map;

    const cleaned = text
        .toLowerCase()
        .replace(/[.,:;!?]/g, ' ')    // quitar puntuación básica
        .trim();

    for (const w of cleaned.split(/\s+/).filter(Boolean)) {
        map.set(w, (map.get(w) || 0) + 1);
    }
    return map;
}