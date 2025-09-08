// mapea lo que venga a una ruta conocida del router
const resolveRoutes = (route) => {
    // si es raíz
    if (route === '/' || route === '') return '/';
    // si es un id corto (1, 2, 12, etc.)
    if (route.length <= 3) return '/:id';
    // por si más adelante agregás otras rutas tipo "/about"
    return `/${route}`;
};
export default resolveRoutes;