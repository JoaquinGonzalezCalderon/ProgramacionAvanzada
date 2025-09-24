function sortByMany(list, specs) {
    const arr = (list ?? []).slice(); // clonar
    const rules = (specs ?? []).map(s => ({
        key: s.key,
        dir: (s.dir || 'asc').toLowerCase() === 'desc' ? -1 : 1
    }));

    arr.sort((a, b) => {
        for (const { key, dir } of rules) {
            const va = a?.[key];
            const vb = b?.[key];
            if (va === vb) continue;
            // Manejo consistente de undefined / null al final
            if (va == null && vb != null) return 1;
            if (vb == null && va != null) return -1;
            if (va < vb) return -1 * dir;
            if (va > vb) return 1 * dir;
        }
        return 0;
    });

    return arr;
}