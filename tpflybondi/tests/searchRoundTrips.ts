import { describe, it, expect } from "vitest";
import { searchRoundTrips } from "@/core/searchRoundTrips";
import type { Flight } from "@/core/types";

describe("searchRoundTrips", () => {
  const base: Flight[] = [
    { origin: "COR", destination: "BRC", price: 300, availability: 3, date: "2025-10-01T10:00:00.000Z" },
    { origin: "BRC", destination: "COR", price: 280, availability: 3, date: "2025-10-05T12:00:00.000Z" },
    { origin: "COR", destination: "BRC", price: 500, availability: 3, date: "2025-10-02T10:00:00.000Z" },
    { origin: "BRC", destination: "COR", price: 310, availability: 1, date: "2025-10-04T12:00:00.000Z" }
  ];

  it("encuentra ida/vuelta con presupuesto y disponibilidad", () => {
    const res = searchRoundTrips(base, 800, 2);
    expect(res.length).toBeGreaterThan(0);
    expect(res[0].totalPrice).toBeLessThanOrEqual(800);
    expect(res[0].nights).toBeGreaterThanOrEqual(1);
  });

  it("filtra por disponibilidad de grupo", () => {
    const res = searchRoundTrips(base, 800, 3);
    // el tramo de 310 tiene avail 1 en la vuelta, debería descartarse;
    // la opción válida queda con 300 + 280
    expect(res[0].priceOut + res[0].priceReturn).toBe(580);
  });

  it("no devuelve si el presupuesto es muy bajo", () => {
    const res = searchRoundTrips(base, 200, 1);
    expect(res.length).toBe(0);
  });
});
