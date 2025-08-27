//funcion declaration
function saludar(nombre) {
    console.log("ASheeeee, " + nombre + "!");

}

saludar("Joaquin");

//funcion expression, mas usada que las declaration

const cliente = function (nombreCliente) {
    console.log("Datos del cliente: " + nombreCliente);

}

cliente("Joaquin");

function actividad(nombre, actividad) {
    console.log("El cliente " + nombre + " esta realizando: " + actividad)
    console.log(`El cliente ${nombre} esta realizando la actividad : ${actividad}`)


}

actividad("Joaquin", "Stripper");
// si la llamamos como actividad () va a utilizar valores por defecto