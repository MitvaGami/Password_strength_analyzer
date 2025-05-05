import React from "react";

export default function AnalysisResult({ result }) {
  if (!result) return null;

  const {
    normalized,
    semantic = [],
    context = { entities: [], year: null },
    heuristic_strength,
    ml_prediction,
  } = result;

  const labels = ["Very Weak", "Weak", "Average", "Strong", "Very Strong"];
  const mlLabel = labels[ml_prediction] ?? `Level ${ml_prediction}`;

  return (
    <div
      className="analysis-result"
      style={{
        padding: 16,
        border: "1px solid #ddd",
        borderRadius: 4,
        background: "#fafafa",
        maxWidth: 500,
      }}
    >
      <h2>Detailed Analysis</h2>
      <p>
        <strong>Normalized:</strong> {normalized}
      </p>
      <p>
        <strong>Semantic Matches:</strong>{" "}
        {semantic.length ? semantic.join(", ") : "None"}
      </p>
      <p>
        <strong>Context Entities:</strong>{" "}
        {context.entities.length ? context.entities.join(", ") : "None"}
      </p>
      <p>
        <strong>Context Year:</strong> {context.year || "N/A"}
      </p>
      <p>
        <strong>Heuristic Score:</strong> {heuristic_strength.toFixed(2)}%
      </p>
      <p>
        <strong>ML Prediction:</strong> {mlLabel}
      </p>
    </div>
  );
}
