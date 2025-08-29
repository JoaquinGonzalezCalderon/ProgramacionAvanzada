// Ejercicio 8: 
// Filtrar y transformar alertas de seguridad
// Dado un array de alertas de seguridad de red, filtra las que sean de nivel "alto" y
// transfórmalas en mensajes para el administrador.

//Ejercicio 8: Filtrar y transformar alertas de seguridad
//Dado un array de alertas de seguridad de red, filtra las que sean de nivel "alto" y
//transfórmalas en mensajes para el administrador.
// Ejercicio 8: Crear un informe de actividad de red con dispositivos y conexiones

const dispositivos = [
  { id: 1, nombre: "PC-Desarrollo", ip: "192.168.1.5",  tipo: "Estación de trabajo" },
  { id: 2, nombre: "PC-Marketing",  ip: "192.168.1.7",  tipo: "Estación de trabajo" },
  { id: 3, nombre: "Servidor-Web",  ip: "192.168.1.10", tipo: "Servidor" },
  { id: 4, nombre: "Servidor-BD",   ip: "192.168.1.11", tipo: "Servidor" }
];

const conexionesActivas = [
  { id: 1, origen: "192.168.1.5", destino: "192.168.1.10", protocolo: "HTTP",  bytes:  8500 },
  { id: 2, origen: "192.168.1.7", destino: "192.168.1.11", protocolo: "MySQL", bytes: 12000 },
  { id: 3, origen: "192.168.1.5", destino: "192.168.1.11", protocolo: "MySQL", bytes:  9200 }
];

// informe que combine la información de dispositivos y conexiones
const informeActividad = conexionesActivas.map(conexion => {
  // dispositivos de origen y destino por IP
  const dispositivoOrigen  = dispositivos.find(d => d.ip === conexion.origen);
  const dispositivoDestino = dispositivos.find(d => d.ip === conexion.destino);

  // retorna información 
  return {
    idConexion: conexion.id,
    protocolo: conexion.protocolo,
    bytes: conexion.bytes,
    origen: dispositivoOrigen
      ? `${dispositivoOrigen.nombre} (${dispositivoOrigen.ip})`
      : conexion.origen,
    destino: dispositivoDestino
      ? `${dispositivoDestino.nombre} (${dispositivoDestino.ip})`
      : conexion.destino
  };
});

console.log("Informe de actividad de red:", informeActividad);

