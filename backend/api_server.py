import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from typing import List
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

import tempfile
import shutil
import asyncio
import os

from scanners.nmap_runner import run_nmap_scan
from scanners.parser_nmap import parse_nmap_xml
from analysis.analyzer import analyze
from reporting.ai_helper import summarize_issues
from reporting.generator import generate_report

app = FastAPI(debug=True)

origins = [
    "http://localhost:3000",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials =True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="Security Scan Assistant API")

@app.post("/scan")
async def start_scan(target: str = Form(...)):
    # start a new Nmap scan and generate a report
    xml_file = run_nmap_scan(target)
    results = parse_nmap_xml(xml_file)
    issues = analyze(results)
    ai_report = summarize_issues(issues)
    report_path = generate_report(ai_report, results, output_file=f"reports/{target}_report.pdf")
    return {"status": "completed", "report_path": str(report_path)}

@app.post("/upload")
async def upload_scan(file: UploadFile):
   # upload an existing Nmap XML file
    temp_path = Path(tempfile.mktemp(suffix=".xml"))
    with temp_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    results = parse_nmap_xml(temp_path)
    issues = analyze(results)
    ai_report = summarize_issues(issues)
    report_path = generate_report(ai_report, results, output_file=f"reports/uploaded_report.pdf")
    return {"status": "completed", "report_path": str(report_path)}

@app.get("/report/{filename}")
async def get_report(filename: str):
    # download generated report PDF
    path = Path(f"reports/{filename}")
    if not path.exists():
        return JSONResponse(status_code=404, content={"error": "File not found"})
    return FileResponse(path, media_type="application/pdf")

@app.get("/")
async def root():
    return {"message": "Security Scan Assistant API running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

