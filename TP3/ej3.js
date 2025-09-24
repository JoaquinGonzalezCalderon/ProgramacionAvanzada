function groupBy(list, keyOrFn) {
    const res = {};
    const getKey = typeof keyOrFn === 'function'
        ? keyOrFn
        : (item) => item?.[keyOrFn];

    for (const item of list ?? []) {
        const k = getKey(item);
        const key = String(k); // garantizar clave de objeto plano
        if (!Object.prototype.hasOwnProperty.call(res, key)) res[key] = [];
        res[key].push(item);
    }
    return res;
}