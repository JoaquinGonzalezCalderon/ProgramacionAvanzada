function pick(obj, keys) {
    const out = {};
    if (!obj || !Array.isArray(keys)) return out;
    for (const k of keys) {
        if (Object.prototype.hasOwnProperty.call(obj, k)) {
            out[k] = obj[k];
        }
    }
    return out;
}