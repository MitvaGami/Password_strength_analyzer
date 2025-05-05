import React, { useState } from "react";
import PasswordInput from "./components/PasswordInput";
import Visualization from "./components/Visualization";
import AnalysisResult from "./components/AnalysisResult";

function App() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch("http://localhost:5000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      if (!res.ok) throw new Error(res.statusText);
      setResult(await res.json());
    } catch (e) {
      setError("Could not analyze password. Is the backend up?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h1>Password Strength Analyzer</h1>

      <PasswordInput
        password={password}
        setPassword={setPassword}
        handleSubmit={handleSubmit}
        loading={loading}
      />

      {error && <div style={{ color: "red", marginBottom: 16 }}>{error}</div>}

      {result && (
        <>
          <Visualization score={result.heuristic_strength} />
          <AnalysisResult result={result} />
        </>
      )}
    </div>
  );
}

export default App;
