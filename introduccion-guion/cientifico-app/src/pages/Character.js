import getData from '../utils/getData';
import getHash from '../utils/getHash';

const Character = async () => {
    const id = getHash();                 // ej: "1"
    const c = await getData(id);          // pide a la API ese personaje

    return `
    <div class="Character-inner">
        <article class="Character-card">
            <img src="${c.image}" alt="${c.name}">
                <h2>${c.name}</h2>
        </article>

        <article class="Character-card">
            <h3>Episodes: <span>${c.episode?.length ?? '-'}</span></h3>
            <h3>Status: <span>${c.status}</span></h3>
            <h3>Species: <span>${c.species}</span></h3>
            <h3>Gender: <span>${c.gender}</span></h3>
            <h3>Origin: <span>${c.origin?.name ?? '-'}</span></h3>
            <h3>Location: <span>${c.location?.name ?? '-'}</span></h3>
        </article>
    </div>
    `;
};

export default Character;