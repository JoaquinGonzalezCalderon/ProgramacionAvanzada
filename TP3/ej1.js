function sumUnique(nums) {
    const seen = new Set();
    let acc = 0;
    for (const x of nums ?? []) {
        if (Number.isFinite(x) && !seen.has(x)) {
            seen.add(x);
            acc += x;
        }
    }
    return acc;
}