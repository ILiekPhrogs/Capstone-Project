import React from "react";
import { getReportUrl } from "../api";

export default function ReportViewer({ reportPath }) {
  const url = getReportUrl(reportPath);

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h2 className="text-xl font-semibold mb-2">Generated Report</h2>
      <iframe
        src={url}
        title="Report PDF"
        width="100%"
        height="600px"
        className="border rounded"
      />
      <div className="mt-3">
        <a
          href={url}
          download
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Download PDF
        </a>
      </div>
    </div>
  );
}
