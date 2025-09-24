import type { Flight, RoundTrip } from "./types";

/**
 * budgetPerPerson: tope por persona (ej: 800)
 * partySize: cantidad de pasajeros (1..4)
 * origins: lista opcional para filtrar por aeropuerto de salida
 */
export function searchRoundTrips(
  flights: Flight[],
  budgetPerPerson = 800,
  partySize = 1,
  origins?: string[]
): RoundTrip[] {
  const byOD = new Map<string, Flight[]>();

  for (const f of flights) {
    const key = `${f.origin}|${f.destination}`;
    if (!byOD.has(key)) byOD.set(key, []);
    byOD.get(key)!.push(f);
  }

  for (const arr of byOD.values()) {
    arr.sort((a, b) => Date.parse(a.date) - Date.parse(b.date));
  }

  const outs = origins?.length ? flights.filter((f) => origins.includes(f.origin)) : flights;
  const results: RoundTrip[] = [];

  for (const o of outs) {
    const retKey = `${o.destination}|${o.origin}`;
    const returns = byOD.get(retKey);
    if (!returns) continue;

    const tOut = Date.parse(o.date);
    for (const r of returns) {
      const tRet = Date.parse(r.date);
      if (tRet <= tOut) continue;
      if (o.availability < partySize || r.availability < partySize) continue;

      const total = o.price + r.price;
      if (total > budgetPerPerson) continue;

      const nights = Math.floor((tRet - tOut) / (1000 * 60 * 60 * 24));
      results.push({
        origin: o.origin,
        destination: o.destination,
        departDate: o.date,
        returnDate: r.date,
        priceOut: o.price,
        priceReturn: r.price,
        totalPrice: total,
        nights,
        availOut: o.availability,
        availReturn: r.availability
      });
    }
  }

  results.sort(
    (a, b) =>
      a.totalPrice - b.totalPrice ||
      b.nights - a.nights ||
      Date.parse(a.departDate) - Date.parse(b.departDate)
  );

  // si querés mostrar solo la mejor por destino, descomenta:
  // const bestByRoute = new Map<string, RoundTrip>();
  // for (const r of results) {
  //   const key = `${r.origin}|${r.destination}`;
  //   if (!bestByRoute.has(key)) bestByRoute.set(key, r);
  // }
  // return [...bestByRoute.values()];

  return results;
}
