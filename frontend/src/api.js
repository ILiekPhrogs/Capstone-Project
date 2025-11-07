import axios from "axios";

const API_URL = "http://localhost:8000";

export async function startScan(target) {
  const form = new FormData();
  form.append("target", target);
  const res = await axios.post(`${API_URL}/scan`, form);
  return res.data;
}

export async function uploadFile(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await axios.post(`${API_URL}/upload`, form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
}

export function getReportUrl(filename) {
  return `${API_URL}/report/${filename}`;
}
