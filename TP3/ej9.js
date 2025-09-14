function debounce(fn, delay) {
    let timer = null;
    return function debounced(...args) {
        const ctx = this;
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
            timer = null;
            fn.apply(ctx, args);
        }, delay);
    };
}