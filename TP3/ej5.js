function deepEqual(a, b) {
    if (a === b) return true;

    // Si uno es null y el otro no 
    if (a === null || b === null) return false;
    if (typeof a !== typeof b) return false;

    // Primitivos (NaN manejo aparte)
    if (typeof a !== 'object') {
        return Number.isNaN(a) && Number.isNaN(b) ? true : a === b;
    }

    // Arrays
    const aIsArr = Array.isArray(a);
    const bIsArr = Array.isArray(b);
    if (aIsArr || bIsArr) {
        if (!(aIsArr && bIsArr)) return false;
        if (a.length !== b.length) return false;
        for (let i = 0; i < a.length; i++) {
            if (!deepEqual(a[i], b[i])) return false;
        }
        return true;
    }

    // Objetos planos
    const ka = Object.keys(a);
    const kb = Object.keys(b);
    if (ka.length !== kb.length) return false;
    // mismo conjunto de claves
    for (const k of ka) {
        if (!Object.prototype.hasOwnProperty.call(b, k)) return false;
        if (!deepEqual(a[k], b[k])) return false;
    }
    return true;
}