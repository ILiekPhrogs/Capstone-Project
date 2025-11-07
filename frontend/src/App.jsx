import React, { useState } from "react";
import axios from "axios";

function App() {
  const [target, setTarget] = useState("");
  const [file, setFile] = useState(null);
  const [pdf, setPdf] = useState(null);

  const handleScan = async () => {
    const formData = new FormData();
    formData.append("target", target);
    const res = await axios.post("http://localhost:8000/scan", formData);
    setPdf(res.data.pdf);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://localhost:8000/upload", formData);
    setPdf(res.data.pdf);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Security Scan Dashboard</h1>
      <div>
        <h3>Start a New Scan</h3>
        <input
          type="text"
          placeholder="Enter target (e.g. 192.168.1.1)"
          value={target}
          onChange={(e) => setTarget(e.target.value)}
        />
        <button onClick={handleScan}>Run Scan</button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <h3>Upload Existing XML File</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload & Analyze</button>
      </div>

      {pdf && (
        <div style={{ marginTop: "40px" }}>
          <h3>Generated Report</h3>
          <a href={`http://localhost:8000/download?pdf_path=${pdf}`} target="_blank" rel="noopener noreferrer">
            View PDF Report
          </a>
        </div>
      )}
    </div>
  );
}

export default App;

