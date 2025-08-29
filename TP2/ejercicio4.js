// Ejercicio 4: 
// Mapear direcciones IP
// Dado un array de servidores con direcciones IP, utiliza el método map() para crear
// un nuevo array que contenga solo las direcciones IP.

const servidores = [
{ nombre: "Servidor Web", ip: "192.168.1.10", sistema: "Linux" },
{ nombre: "Servidor de Base de Datos", ip: "192.168.1.11", sistema: "Windows" },
{ nombre: "Servidor de Correo", ip: "192.168.1.12", sistema: "Linux" },
{ nombre: "Servidor DNS", ip: "192.168.1.13", sistema: "Linux" },
{ nombre: "Servidor de Archivos", ip: "192.168.1.14", sistema: "Windows" }
];

const mapeado = servidores.map(obtieneip)

function obtieneip(ips) {
    return [ips.ip].join("")
}


console.log("Nuevo array con las IP:" ,mapeado)