import React from "react";

export default function Visualization({ score }) {
  const pct = Math.min(100, Math.max(0, Math.round(score * 100) / 100));

  return (
    <div className="visualization" style={{ marginBottom: 20 }}>
      <p>
        Password Strength: <strong>{pct}%</strong>
      </p>
      <progress
        value={pct}
        max="100"
        style={{ width: "100%", maxWidth: 400 }}
      />
    </div>
  );
}
