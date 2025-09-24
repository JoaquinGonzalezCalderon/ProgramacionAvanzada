// src/utils/getHash.js
const getHash = () => {
    // Convierte:
    //   "#/5eb87d47ffd86e000604b388/" -> "5eb87d47ffd86e000604b388"
    //   "#/" o "" -> "/"
    const hash = window.location.hash || '#/';
    const cleaned = hash
        .replace(/^#\/?/, '')  // saca "#/" o "#"
        .replace(/\/$/, '');   // saca la barra final

    return cleaned || '/';
};

export default getHash;
