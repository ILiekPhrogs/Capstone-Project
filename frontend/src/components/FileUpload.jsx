import React, { useState } from "react";
import { uploadFile } from "../api";

export default function FileUpload({ onReportReady }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const res = await uploadFile(file);
    onReportReady(res.report_path.split("/").pop());
    setLoading(false);
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-2">Upload Existing Scan</h2>
      <input
        type="file"
        accept=".xml"
        onChange={e => setFile(e.target.files[0])}
        className="block mb-3"
      />
      <button
        className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Processing..." : "Upload & Analyze"}
      </button>
    </div>
  );
}
