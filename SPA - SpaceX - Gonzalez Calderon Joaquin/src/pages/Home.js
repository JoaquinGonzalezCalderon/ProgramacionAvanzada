import getLaunch from '../utils/getLaunch.js';


const Home = async () => {
  let launches = await getLaunch(); // Array de lanzamientos

  // quedate sólo con los que tienen imagen de patch
  launches = launches.filter(l => l?.links?.patch?.small);

  // orden descendente por fecha
  launches.sort((a, b) => new Date(b.date_utc) - new Date(a.date_utc));

  const view = `
    <div class="Characters">
      ${launches.map(l => {
    const img = l.links.patch.small;
    const name = l.name || 'Sin nombre';
    const date = l.date_utc ? new Date(l.date_utc).toLocaleDateString('es-AR') : '—';

    // badge estado: success true/false/null
    const status = l.success === true ? 'success' : (l.success === false ? 'fail' : 'tbd');
    const statusText = l.success === true ? 'Éxito' : (l.success === false ? 'Falla' : 'TBD');

    return `
          <article class="Characters-item">
            <a href="#/${l.id}/" class="card-link">
              <img src="${img}" alt="${name}" />
              <div class="card-meta">
                <h2>${name}</h2>
                <div class="meta-row">
                  <span class="badge ${status}">${statusText}</span>
                  <span class="date">${date}</span>
                </div>
              </div>
            </a>
          </article>
        `;
  }).join('')}
    </div>
  `;
  return view;
};

export default Home;
