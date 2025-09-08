// devuelve el id del hash: "#/1" -> "1", y "/" si no hay
const getHash = () => {
    const hash = location.hash.slice(1).toLowerCase(); // "/1" o "/"
    const parts = hash.split('/');                      // ["", "1"]
    return parts[1] || '/';
};
export default getHash;