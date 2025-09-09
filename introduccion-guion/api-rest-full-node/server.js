// importar express
const express = require('express');

// crear una instancia de express
const app = express();

const port = 3000;

//crear una ruta
app.get('/', (req, res) => {
    res.json({
        message: 'Hola Mundo'
    });
});

app.listen(port, () => {
    console.log(`Servidor corriendo en http://localhost:${port}`);

});