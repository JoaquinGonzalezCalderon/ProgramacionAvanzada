const formatDate = (isoUTC) => {
    if (!isoUTC) return 'N/D';
    try {
        const d = new Date(isoUTC);
        return d.toLocaleString('es-AR', {
            dateStyle: 'short',
            timeStyle: 'medium'
        });
    } catch {
        return 'N/D';
    }
};
export default formatDate;
