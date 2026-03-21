import React, { useState } from "react";
import axios from "axios";

function App() {
  const [resume, setResume] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!resume.trim()) {
      setError("Please paste a resume");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        resume_text: resume,
      });
      
      setResult(response.data);
      
      // Check for backend error
      if (response.data.error) {
        setError(response.data.error);
        setResult(null);
      }
    } catch (err) {
      setError("Failed to connect to server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "800px", margin: "0 auto" }}>
      <h1>LoomGraph 🚀</h1>
      
      <textarea
        rows="8"
        cols="80"
        placeholder="Paste your resume here..."
        value={resume}
        onChange={(e) => setResume(e.target.value)}
        disabled={loading}
        style={{ width: "100%", padding: "12px", fontSize: "14px" }}
      />
      
      <br /><br />
      
      <button 
        onClick={handleSubmit}
        disabled={loading || !resume.trim()}
        style={{
          padding: "12px 24px",
          fontSize: "16px",
          backgroundColor: loading ? "#ccc" : "#007bff",
          color: "white",
          border: "none",
          borderRadius: "6px",
          cursor: loading ? "not-allowed" : "pointer"
        }}
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {error && (
        <div style={{ 
          marginTop: "20px", 
          padding: "12px", 
          backgroundColor: "#fee", 
          border: "1px solid #fcc",
          borderRadius: "6px",
          color: "#c33"
        }}>
          {error}
        </div>
      )}

      {result && !error && (
        <div style={{ marginTop: "30px" }}>
          <h3>🎯 Detected Role: <strong>{result.detected_role}</strong></h3>
          
          <div style={{ margin: "20px 0" }}>
            <strong>Skills Found:</strong>
            {result.skills.map((s, i) => (
              <span 
                key={i} 
                style={{ 
                  backgroundColor: "lightgreen", 
                  margin: "4px", 
                  padding: "4px 8px",
                  borderRadius: "12px",
                  fontSize: "14px"
                }}
              >
                {s}
              </span>
            ))}
          </div>

          <div style={{ margin: "20px 0" }}>
            <strong>Skill Gap:</strong>
            {result.skill_gap.length === 0 ? (
              <span style={{ color: "green" }}>None! You're ready! 🎉</span>
            ) : (
              result.skill_gap.map((s, i) => (
                <span 
                  key={i} 
                  style={{ 
                    backgroundColor: "#fee", 
                    color: "red",
                    margin: "4px", 
                    padding: "4px 8px",
                    borderRadius: "12px"
                  }}
                >
                  {s}
                </span>
              ))
            )}
          </div>

          <p style={{ fontSize: "18px", fontWeight: "bold" }}>
            Readiness Score: <span style={{ color: result.readiness_score > 70 ? "green" : "orange" }}>
              {result.readiness_score}%
            </span>
          </p>

          {result.learning_path && (
            <div style={{ marginTop: "25px" }}>
              <h3>📚 Personalized Learning Path</h3>
              <div style={{
                backgroundColor: "#1e1e1e",
                padding: "20px",
                borderRadius: "10px",
                color: "white",
                whiteSpace: "pre-line",
                lineHeight: "1.7",
                fontFamily: "monospace"
              }}>
                {result.learning_path}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
