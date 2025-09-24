import React from "react";

type Props = { value: number; onChange: (n: number) => void; min?: number; max?: number };

export default function PartySizePicker({ value, onChange, min = 1, max = 4 }: Props) {
  return (
    <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
      <label style={{ fontSize: 18 }}>Personas</label>
      <button
        onClick={() => onChange(Math.max(min, value - 1))}
        aria-label="disminuir"
      >
        −
      </button>
      <strong style={{ fontSize: 18, width: 24, textAlign: "center" }}>{value}</strong>
      <button
        onClick={() => onChange(Math.min(max, value + 1))}
        aria-label="aumentar"
      >
        +
      </button>
    </div>
  );
}
