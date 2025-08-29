// Ejercicio 10: 
// Analizar y optimizar topología de red
// Dado un objeto que representa una topología de red, encuentra los nodos con
// más conexiones y sugiere optimizaciones.

const topologiaRed2 = {
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

function contarConexiones(topologia) {
  const contador = Object.fromEntries(topologia.nodos.map(n => [n.id, 0]));
  topologia.conexiones.forEach(({ origen, destino }) => {
    contador[origen]++; 
    contador[destino]++;
  });
  return contador;
}

function ordenarNodosPorConexiones(conexionesPorNodo) {
  return Object.entries(conexionesPorNodo).sort((a, b) => b[1] - a[1]);
}

function sugerirOptimizaciones(topologia, conexionesPorNodo, umbralConex = 2, umbralBajoBW = 200) {
  const sugerencias = [];

  // nodos muy conectados
  Object.entries(conexionesPorNodo).forEach(([id, count]) => {
    if (count > umbralConex) {
      sugerencias.push(`Nodo ${id} con ${count} conexiones: considerar link aggregation, uplinks de mayor capacidad o segmentación/VLANs.`);
    }
  });

  // 2) enlaces de bajo ancho de banda que tocan nodos críticos
  const nodosAltos = new Set(
    Object.entries(conexionesPorNodo).filter(([_, c]) => c > umbralConex).map(([id]) => id)
  );

  topologia.conexiones.forEach(({ origen, destino, ancho_banda }) => {
    const tocaCritico = nodosAltos.has(origen) || nodosAltos.has(destino);
    if (tocaCritico && ancho_banda < umbralBajoBW) {
      sugerencias.push(`Enlace ${origen}↔${destino} con ${ancho_banda} Mbps < ${umbralBajoBW} Mbps: evaluar upgrade.`);
    }
  });

  return sugerencias;
}

//análisis
const conexionesPorNodo2 = contarConexiones(topologiaRed2);
const nodosOrdenados2   = ordenarNodosPorConexiones(conexionesPorNodo2);
const sugerencias2      = sugerirOptimizaciones(topologiaRed2, conexionesPorNodo2);

console.log("Conexiones por nodo (v2):", conexionesPorNodo2);
console.log("Nodos ordenados (v2):", nodosOrdenados2);
console.log("Sugerencias (v2):", sugerencias2);
