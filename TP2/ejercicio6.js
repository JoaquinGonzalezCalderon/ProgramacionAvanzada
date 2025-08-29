// Ejercicio 6: 
// Calcular estadísticas de red
// Dado un objeto con estadísticas de tráfico de red por hora, calcula el total de
// datos transferidos y la hora con mayor tráfico.

const traficoRed = {
  "08:00": 1250,
  "09:00": 1870,
  "10:00": 2100,
  "11:00": 1950,
  "12:00": 1600,
  "13:00": 1300,
  "14:00": 1700,
  "15:00": 2200,
  "16:00": 1800,
  "17:00": 1500
};

// total de mb
const totalMB = Object.values(traficoRed)
  .reduce((acc, mb) => acc + mb, 0);

// hora con mayor trafico

const [horaPico, mbPico] = Object.entries(traficoRed)
  .reduce((maxPar, parActual) => {
    const [, mbMax] = maxPar;
    const [, mbAct] = parActual;
    return mbAct > mbMax ? parActual : maxPar;
  });


console.log("Total MB:", totalMB);

console.log("Hora con mayor trafico:", horaPico, "con", mbPico, "MB");