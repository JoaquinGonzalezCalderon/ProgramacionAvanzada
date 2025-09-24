// importar express
const express = require('express');

// crear una instancia de express

const app = express();

const PORT = process.env.PORT || 3000;

//crear una ruta
app.use(express.json());

// base de datos en memoria (se pierde cuando se detiene el servidor)
const users = [];
let nextId = 1;


app.get('/users', (req, res) => {
    res.json(users);
});

app.get('/users/:id', (req, res) => {
    const id = Number(req.params.id);
    const user = users.find((user) => user.id === id);
    if (!user) {
        return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    res.json(user);
});

//POST /users
// Crear un nuevo usuario
// Body JSON esperado: { name: string, email: string }

app.post('/users', (req, res) => {
    const { name, email } = req.body || {};

    if (!name || !email) {
        return res.status(400).json({ error: 'Nombre y email son requeridos' });
    }
    // El operador ++ incrementa el valor de nextId en 1 después de usarlo.
    // Es decir, asigna el valor actual de nextId a id, y luego suma 1 a nextId.
    const newUser = {
        id: nextId++,
        name,
        email,
        createdAt: new Date().toISOString()
    };
    users.push(newUser);
    res.status(201).json(newUser);

});

// Para usar esta función en Postman:
// 1. Selecciona el método DELETE.
// 2. Usa la URL: http://localhost:3000/users/{id}  (reemplaza {id} por el id del usuario que quieres eliminar)
// 3. No necesitas enviar body, solo la URL con el id.
//
// Ejemplo: DELETE http://localhost:3000/users/2
//
// Si Postman queda "en espera", probablemente falta enviar una respuesta desde el servidor.
// Asegúrate de que la función envía una respuesta con res.json o res.send.

app.delete('/users/:id', (req, res) => {
    const id = Number(req.params.id);
    const index = users.findIndex((user) => user.id === id);
    if (index === -1) {
        return res.status(404).json({ error: 'Usuario no encontrado' });
    }
    users.splice(index, 1);
    res.json({ message: 'Usuario eliminado correctamente' });
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);

});