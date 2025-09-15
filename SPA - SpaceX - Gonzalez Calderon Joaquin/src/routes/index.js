// src/routes/index.js
import Header from '../templates/Header';
import Home from '../pages/Home';
import Launch from '../pages/Launch';
import Error404 from '../pages/Error404';

import getHash from '../utils/getHash';
import resolveRoutes from '../utils/resolveRoutes';

const routes = {
    '/': Home,
    '/:id': Launch,
};

const router = async () => {
    try {
        const header = document.getElementById('header');
        const content = document.getElementById('content');

        if (!header || !content) {
            // Si falta alguno de los contenedores, no vamos a poder renderizar nada
            document.body.innerHTML = `
        <p style="padding:16px">Error de plantilla: faltan contenedores <code>#header</code> y/o <code>#content</code>.</p>
      `;
            return;
        }

        // Header
        header.innerHTML = await Header();

        // Loader
        content.innerHTML = `
      <div style="display:flex;justify-content:center;padding:24px">
        <div class="Main-loading" aria-label="Cargando"></div>
      </div>
    `;

        // Ruta
        const hash = getHash();            // "…" o "/"
        const route = resolveRoutes(hash); // "/" o "/:id"
        const render = routes[route] || Error404;

        // Render final
        const html = await render();
        content.innerHTML = html;
    } catch (err) {
        console.error('[router] Error:', err);
        const content = document.getElementById('content');
        if (content) {
            content.innerHTML = `
        <div style="padding:24px">
          <h2>Ocurrió un error</h2>
          <pre style="white-space:pre-wrap;background:#f5f5f5;padding:12px;border-radius:8px">${String(err)}</pre>
          <p><a href="#/">Volver al inicio</a></p>
        </div>
      `;
        }
    }
};

export default router;
