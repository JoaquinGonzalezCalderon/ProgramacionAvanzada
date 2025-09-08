import Header from '../templates/Header';
import Home from '../pages/Home';
import Character from '../pages/Character';
import Error404 from '../pages/Error404';

import getHash from '../utils/getHash';
import resolveRoutes from '../utils/resolveRoutes';

const routes = {
    '/': Home,
    '/:id': Character,
};

const router = async () => {
    const header = document.getElementById('header');
    const content = document.getElementById('content');

    header.innerHTML = await Header();

    const hash = getHash();                // "1" o "/"
    const route = resolveRoutes(hash);     // "/" o "/:id"
    const render = routes[route] || Error404;

    content.innerHTML = await render();
};

export default router;