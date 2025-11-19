import React, { useState } from "react";
import { startScan } from "../api";

export default function ScanForm({ onReportReady }) {
  const [target, setTarget] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    const res = await startScan(target);
    onReportReady(res.report_path.split("/").pop());
    setLoading(false);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-2">Start New Scan</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          className="border p-2 w-full mb-3"
          placeholder="Enter target (e.g., 192.168.0.1)"
          value={target}
          onChange={e => setTarget(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Scanning..." : "Start Scan"}
        </button>
      </form>
    </div>
  );
}
