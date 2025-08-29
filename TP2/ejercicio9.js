// Ejercicio 9: 
// Combinar datos de dispositivos y conexiones
// Combina información de dispositivos y conexiones para crear un informe
// detallado de la actividad de red.

const topologiaRed = {
  nodos: [
    { id: "A", tipo: "Router", ubicacion: "Planta 1" },
    { id: "B", tipo: "Switch", ubicacion: "Planta 1" },
    { id: "C", tipo: "Switch", ubicacion: "Planta 2" },
    { id: "D", tipo: "Switch", ubicacion: "Planta 3" },
    { id: "E", tipo: "Router", ubicacion: "Planta 3" }
  ],
  conexiones: [
    { origen: "A", destino: "B", ancho_banda: 1000 },
    { origen: "A", destino: "C", ancho_banda: 1000 },
    { origen: "B", destino: "C", ancho_banda: 100 },
    { origen: "B", destino: "D", ancho_banda: 100 },
    { origen: "C", destino: "D", ancho_banda: 100 },
    { origen: "C", destino: "E", ancho_banda: 1000 },
    { origen: "D", destino: "E", ancho_banda: 1000 }
  ]
};

// inicialización
const conexionesPorNodo = {};
topologiaRed.nodos.forEach(nodo => { conexionesPorNodo[nodo.id] = 0; });

// contar conexiones
topologiaRed.conexiones.forEach(({ origen, destino }) => {
  if (conexionesPorNodo[origen] !== undefined) conexionesPorNodo[origen]++;
  if (conexionesPorNodo[destino] !== undefined) conexionesPorNodo[destino]++;
});

// ordenar desc por cantidad de conexiones
const nodosOrdenados = Object.entries(conexionesPorNodo)
  .sort((a, b) => b[1] - a[1]); // [id, cantidad]

// sugerencias 
const UMBRAL_CONEX = 2;
const sugerencias = nodosOrdenados
  .filter(([_, count]) => count > UMBRAL_CONEX)
  .map(([id, count]) => `Nodo ${id} tiene ${count} conexiones: evaluar más ancho de banda, uplinks agregados o segmentación.`);

console.log("Conexiones por nodo:", conexionesPorNodo);
console.log("Nodos ordenados por número de conexiones:", nodosOrdenados);
console.log("Sugerencias de optimización:", sugerencias);
