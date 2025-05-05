import React from "react";

export default function PasswordInput({
  password,
  setPassword,
  handleSubmit,
  loading,
}) {
  const onSubmit = (e) => {
    e.preventDefault();
    handleSubmit();
  };

  return (
    <form onSubmit={onSubmit} className="password-input">
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter your password"
        disabled={loading}
        style={{ padding: "8px", fontSize: "1rem" }}
      />
      <button
        type="submit"
        disabled={!password || loading}
        style={{ marginLeft: "8px", padding: "8px 16px" }}
      >
        {loading ? "Analyzing…" : "Analyze"}
      </button>
    </form>
  );
}
