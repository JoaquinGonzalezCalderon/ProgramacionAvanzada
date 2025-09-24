import React from "react";
import { useNavigate } from "react-router-dom";
import PartySizePicker from "@/components/PartySizePicker";

export default function Home() {
  const nav = useNavigate();
  const [partySize, setPartySize] = React.useState(1);
  const budget = 800; // fijo según enunciado

  return (
    <main style={{ maxWidth: 720, margin: "40px auto", padding: "0 16px" }}>
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>
        ¿A dónde puedo ir con ${budget} (ida y vuelta)?
      </h1>
      <p style={{ fontSize: 18 }}>Elegí cuántas personas viajan y te mostramos lo que te alcanza.</p>

      <section style={{ border: "1px solid #eee", borderRadius: 12, padding: 16, marginTop: 16 }}>
        <PartySizePicker value={partySize} onChange={setPartySize} />
        <div style={{ marginTop: 16 }}>
          <button
            style={{ fontSize: 18, padding: "10px 16px", borderRadius: 10 }}
            onClick={() => nav(`/results?party=${partySize}&budget=${budget}`)}
          >
            Ver destinos que me alcanzan
          </button>
        </div>
        <p style={{ marginTop: 12, color: "#666" }}>No importa el día: te mostramos la mejor combinación (más barata primero).</p>
      </section>
    </main>
  );
}
