const carrito = ['Producto 1', 'Producto 2', 'Producto 3'];

console.log(carrito);

carrito.map(producto => {
    return `El producto es: ${producto}`;

})

//spread operator

let lenguajes = ['asheeee', 'instaaaaa'];
let fremaworksas = ['asheeee', 'instaaaaa'];

//unir los 2 arrays en unos solo

let tecnologias = [...lenguajes, ...fremaworksas];

console.log(tecnologias);