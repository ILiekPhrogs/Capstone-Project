# CyberScan Assistant by Raquel Woolsey 
A Python-based vulnerability analysis assistant that parses security scan results, classifies vulnerabilities, enriches findings with CVE/CVSS data, and generates clear, professional reports.

**LEGAL WARNING**

**Unauthorized scanning of networks, systems, or devices that you do not own *or* do not have written permission to test is illegal.**  
Laws such as the Computer Fraud and Abuse Act (CFAA), state cybercrime statutes, and similar international regulations carry heavy penalties including fines, termination of employment, and criminal charges.

**Use this tool only on environments you own, administer, or have explicit written authorization to scan.  
The author assumes no liability for misuse.**

---

CyberScan Assistant streamlines vulnerability analysis by:
-Parsing scan files from tools like **Nmap (XML)** 
-Normalizing results into a consistent **Vulnerability** model 
-Enriching findings using service banners, CVE lookups, and heuristics
-Classifying vulnerabilities using a **rule-based or ML model**
-Generating clear, easy-to-understand summaries and reports  
-running from from the CLI (`main.py`) (for now)

#Project Structure

/Capstone Project
  -main.py
  -config.py
  -utils.py
  -api_server.py
  /analysis
    -analyzer.py
  /reporting
    -ai_helper.py
    -generator.py
  /scanners
    -nmap_runner.py
    -parser_nmap.py
  /venv

#How to use
1. Clone repo and cd "Capstone Project'
2. Create and activate a virtual environment (recommended) 
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
3.Install dependencies 
reportlab, fastAPI, uvicorn, openAI
4.Run a scan file or Run a live Nmap scan
python3 main.py --file scan.xml
python3 main.py --scan 127.0.0.1



