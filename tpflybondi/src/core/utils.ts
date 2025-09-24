import { z } from "zod";
import type { Flight } from "./types";

const FlightSchema = z.object({
  origin: z.string(),
  destination: z.string(),
  price: z.number(),
  availability: z.number().int().nonnegative(),
  date: z.string().refine((s) => !Number.isNaN(Date.parse(s)), "date inválida")
});

export async function getFlights(): Promise<Flight[]> {
  const res = await fetch("/dataset.json", { cache: "no-store" });
  if (!res.ok) throw new Error("No se pudo cargar dataset.json");
  const data = await res.json();
  const parsed = z.array(FlightSchema).safeParse(data);
  if (!parsed.success) {
    console.error(parsed.error.flatten());
    throw new Error("Dataset no válido");
  }
  return parsed.data;
}

export function fmtCurrency(n: number) {
  return new Intl.NumberFormat("es-AR", { style: "currency", currency: "USD", maximumFractionDigits: 2 }).format(n);
}

export function toLocalStr(iso: string) {
  const d = new Date(iso);
  return d.toLocaleString("es-AR", { dateStyle: "medium", timeStyle: "short" });
}
