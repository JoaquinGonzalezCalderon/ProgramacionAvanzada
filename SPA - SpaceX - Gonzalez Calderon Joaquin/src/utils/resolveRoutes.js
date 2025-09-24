// src/utils/resolveRoutes.js
// Mapea "/" a Home y cualquier otro string a "/:id"
const resolveRoutes = (route) => {
    if (route === '/' || route.length === 0) return '/';
    return '/:id';
};

export default resolveRoutes;
