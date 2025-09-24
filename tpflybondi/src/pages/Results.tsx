import React from "react";
import { useSearchParams, Link } from "react-router-dom";
import { getFlights } from "@/core/utils";
import { searchRoundTrips } from "@/core/searchRoundTrips";
import type { RoundTrip } from "@/core/types";
import ResultCard from "@/components/ResultCard";

export default function Results() {
  const [params] = useSearchParams();
  const budget = Number(params.get("budget") ?? 800);
  const party = Math.max(1, Math.min(4, Number(params.get("party") ?? 1)));

  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [rows, setRows] = React.useState<RoundTrip[]>([]);

  React.useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const flights = await getFlights();
        const res = searchRoundTrips(flights, budget, party);
        setRows(res);
        setError(null);
      } catch (e: any) {
        setError(e?.message ?? "Error");
      } finally {
        setLoading(false);
      }
    })();
  }, [budget, party]);

  return (
    <main style={{ maxWidth: 720, margin: "40px auto", padding: "0 16px" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ fontSize: 24, margin: 0 }}>Resultados</h1>
        <Link to="/">◀ Volver</Link>
      </header>

      <p style={{ marginTop: 8 }}>Presupuesto por persona: <strong>${budget}</strong> — Personas: <strong>{party}</strong></p>

      {loading && <p>Cargando opciones…</p>}
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      {!loading && !error && rows.length === 0 && (
        <p>No encontramos combinaciones que cumplan con tu presupuesto y disponibilidad.</p>
      )}

      {!loading && !error && rows.slice(0, 30).map((r, i) => (
        <ResultCard key={i} r={r} partySize={party} />
      ))}
    </main>
  );
}
