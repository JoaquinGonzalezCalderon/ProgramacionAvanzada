function withTimeout(promise, ms) {
    return new Promise((resolve, reject) => {
        const id = setTimeout(() => reject(new Error('Timeout')), ms);
        Promise.resolve(promise)
            .then((v) => { clearTimeout(id); resolve(v); })
            .catch((e) => { clearTimeout(id); reject(e); });
    });
}
// // Ejemplo:
// // withTimeout(fetch('/api'), 1000).then(...).catch(console.error);

// 10B) allSettledLite: versión sin Promise.allSettled
function allSettledLite(promises) {
    const wrap = (p) =>
        Promise.resolve(p)
            .then((value) => ({ status: 'fulfilled', value }))
            .catch((reason) => ({ status: 'rejected', reason }));

    return Promise.all((promises ?? []).map(wrap));
}