import React, { useState } from "react";
import ScanForm from "./ScanForm";
import FileUpload from "./FileUpload";
import ReportViewer from "./ReportViewer";

export default function Dashboard() {
  const [reportPath, setReportPath] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-4">Security Scan Dashboard</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <ScanForm onReportReady={setReportPath} />
        <FileUpload onReportReady={setReportPath} />
      </div>

      {reportPath && (
        <div className="mt-10">
          <ReportViewer reportPath={reportPath} />
        </div>
      )}
    </div>
  );
}
