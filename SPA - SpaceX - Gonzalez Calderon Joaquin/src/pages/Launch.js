// src/pages/Launch.js
import getHash from '../utils/getHash.js';
import getLaunch from '../utils/getLaunch.js';
import formatDate from '../utils/formatDate.js'; // si no lo tenés, podés quitarlo y usar toLocaleString

function renderFailures(failures = []) {
  if (!Array.isArray(failures) || failures.length === 0) {
    return '<li>Sin fallas registradas</li>';
  }
  return failures
    .map((f, i) => {
      const reason = f?.reason || 'N/D';
      const time = (f?.time ?? 'N/D');
      return `<li><strong>Falla ${i + 1}:</strong> ${reason} (tiempo: ${time})</li>`;
    })
    .join('');
}

const Launch = async () => {
  const id = getHash();              // p.ej. "5eb87d47ffd86e000604b388"
  const launch = await getLaunch(id);

  if (!launch || typeof launch !== 'object') {
    return `
      <div class="Error404">
        <h2>No se encontró el lanzamiento</h2>
        <p><a href="#/">Volver al inicio</a></p>
      </div>
    `;
  }

  const name = launch?.name ?? 'Sin nombre';
  const img = launch?.links?.patch?.small || '';
  const flight = launch?.flight_number ?? 'N/D';
  const date = formatDate
    ? formatDate(launch?.date_utc)
    : (launch?.date_utc ? new Date(launch.date_utc).toLocaleString('es-AR', { dateStyle: 'short', timeStyle: 'medium' }) : 'N/D');
  const details = launch?.details || 'Sin detalles';

  const links = launch?.links || {};
  const extras = [];
  if (links?.webcast) extras.push(`<a href="${links.webcast}" target="_blank" rel="noopener">Ver webcast</a>`);
  if (links?.article) extras.push(`<a href="${links.article}" target="_blank" rel="noopener">Artículo</a>`);
  if (links?.wikipedia) extras.push(`<a href="${links.wikipedia}" target="_blank" rel="noopener">Wikipedia</a>`);
  const extrasHTML = extras.length ? `<p>${extras.join(' · ')}</p>` : '<p>—</p>';

  const view = `
    <div class="Characters-inner">
      <article class="Characters-card">
        <img src="${img}" alt="${name}" />
        <h2>${name}</h2>
      </article>

      <article class="Characters-card">
        <h3>Detalles</h3>
        <p>${details}</p>

        <h3>Información</h3>
        <ul>
          <li><strong>N° de vuelo:</strong> ${flight}</li>
          <li><strong>Fecha/Hora:</strong> ${date}</li>
        </ul>

        <h3>Fallas</h3>
        <ul>${renderFailures(launch?.failures)}</ul>

        <h3>Enlaces</h3>
        ${extrasHTML}
      </article>
    </div>
  `;
  return view;
};

export default Launch;   // 👈 importante: exportar Launch, no Character
