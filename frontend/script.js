// Frontend test console for FastAPI endpoints


const apiBaseUrl = `${window.location.protocol}//${window.location.host}`;


const statusBtn = document.getElementById("btn-status");
const statusOut = document.getElementById("status-output");


const scanForm = document.getElementById("scan-form");
const scanTargetInput = document.getElementById("scan-target");
const scanOut = document.getElementById("scan-output");


const uploadForm = document.getElementById("upload-form");
const uploadFileInput = document.getElementById("upload-file");
const uploadOut = document.getElementById("upload-output");


const reportForm = document.getElementById("report-form");
const reportFilenameInput = document.getElementById("report-filename");
const reportOut = document.getElementById("report-output");


let lastReportName = "";


function pretty(obj) {
  try {
    if (typeof obj === "string") {
      return obj;
    }
    return JSON.stringify(obj, null, 2);
  } catch {
    return String(obj);
  }
}


async function handleResponse(res) {
  const contentType = res.headers.get("content-type") || "";
  if (!res.ok) {
    let errorBody = "";
    try {
      if (contentType.includes("application/json")) {
        const json = await res.json();
        errorBody = `\n${JSON.stringify(json, null, 2)}`;
      } else {
        const text = await res.text();
        errorBody = `\n${text}`;
      }
    } catch {
      // ignore
    }
    throw new Error(`HTTP ${res.status}${errorBody}`);
  }


  if (contentType.includes("application/json")) {
    return res.json();
  }
  return res;
}


statusBtn?.addEventListener("click", async () => {
  statusOut.textContent = ">>> Pinging API...";
  try {
    const res = await fetch(`${apiBaseUrl}/`);
    const data = await handleResponse(res);
    statusOut.textContent = pretty(data);
  } catch (err) {
    statusOut.textContent = `ERROR:\n${err.message || err}`;
  }
});


scanForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const target = scanTargetInput.value.trim();
  if (!target) {
    scanOut.textContent = "ERROR: Target is required.";
    return;
  }


  scanOut.textContent = `>>> Launching scan on ${target}...`;


  try {
    const formData = new FormData();
    formData.append("target", target);


    const res = await fetch(`${apiBaseUrl}/scan`, {
      method: "POST",
      body: formData,
    });
    const data = await handleResponse(res);
    scanOut.textContent = pretty(data);


    if (data && data.report_path) {
      const parts = String(data.report_path).split("/");
      lastReportName = parts[parts.length - 1];
      if (!reportFilenameInput.value) {
        reportFilenameInput.value = lastReportName;
      }
    }
  } catch (err) {
    scanOut.textContent = `ERROR:\n${err.message || err}`;
  }
});


uploadForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  uploadOut.textContent = ">>> Uploading XML telemetry...";


  const file = uploadFileInput.files[0];
  if (!file) {
    uploadOut.textContent = "ERROR: Please choose an .xml file first.";
    return;
  }


  try {
    const formData = new FormData();
    formData.append("file", file);


    const res = await fetch(`${apiBaseUrl}/upload`, {
      method: "POST",
      body: formData,
    });
    const data = await handleResponse(res);
    uploadOut.textContent = pretty(data);


    if (data && data.report_path) {
      const parts = String(data.report_path).split("/");
      lastReportName = parts[parts.length - 1];
      if (!reportFilenameInput.value) {
        reportFilenameInput.value = lastReportName;
      }
    }
  } catch (err) {
    uploadOut.textContent = `ERROR:\n${err.message || err}`;
  }
});


reportForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const filename = reportFilenameInput.value.trim();
  if (!filename) {
    reportOut.textContent = "ERROR: Please enter a report filename.";
    return;
  }


  reportOut.textContent = `>>> Requesting dossier: ${filename}...`;


  try {
    const res = await fetch(`${apiBaseUrl}/report/${encodeURIComponent(filename)}`);
    if (res.status === 404) {
      reportOut.textContent = "ERROR: Report not found (404).";
      return;
    }


    await handleResponse(res); // will throw on non-2xx


    const blob = await res.blob();
    const url = URL.createObjectURL(blob);


    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);


    reportOut.textContent = `SUCCESS: Downloaded ${filename} (${blob.size} bytes).`;
  } catch (err) {
    reportOut.textContent = `ERROR:\n${err.message || err}`;
  }
});




