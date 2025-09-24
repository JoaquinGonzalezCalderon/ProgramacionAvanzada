import React from "react";
import type { RoundTrip } from "@/core/types";

export default function ResultCard({ r, partySize }: { r: RoundTrip; partySize: number }) {
  return (
    <article style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginTop: 12 }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
        <strong>{r.origin} → {r.destination}</strong>
        <span>{r.nights} noches</span>
      </header>

      <div style={{ marginTop: 8, display: "flex", gap: 12, flexWrap: "wrap" }}>
        <div>
          <div>Ida: {new Date(r.departDate).toLocaleString("es-AR", { dateStyle: "medium", timeStyle: "short" })}</div>
          <div>Vuelta: {new Date(r.returnDate).toLocaleString("es-AR", { dateStyle: "medium", timeStyle: "short" })}</div>
        </div>
        <div>
          <div>Precio ida: ${r.priceOut}</div>
          <div>Precio vuelta: ${r.priceReturn}</div>
        </div>
        <div>
          <div>Total por persona: <strong>${r.totalPrice}</strong></div>
          <div>Total grupo ({partySize}): <strong>${r.totalPrice * partySize}</strong></div>
        </div>
      </div>
    </article>
  );
}


