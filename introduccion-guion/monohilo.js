// console.log("Hola")
// setInterval(function () {
//     console.log("Sigo activo luca saboredo")
// }, 1000);

// console.log(process.argv);
//te dice donde esta el archivo

// console.log(__dirname)
//se usa para mapear y redirigir archivos

// console.log(__filename)

const fs = require('fs')

function leer(ruta, cb) {
    fs.readFile(ruta, 'utf-8', (err, data) => {
        if (err) {
            cb('Error: ' + err.message);
        } else {
            cb(null, data);
        }
    });
}

leer(__dirname + '/archivo.txt', (error, contenido) => {
    if (error) {
        console.log(error);
    } else {
        console.log(contenido);
    }
});