from collections import defaultdict

RISKY_PORTS = {
    "21": ("FTP", "High", "FTP transmits credentials in cleartext; consider disabling or enforcing SFTP/FTPS"),
    "23": ("Telnet", "High", "Telnet is unencrypted; use SSH instead"),
    "139": ("NetBIOS-SSN", "High", "Legacy Windows file sharing/printing"),
    "445": ("SMB", "High", "SMB services can expose files; ensure patches and SMB signing"),
    "3389": ("RDP", "High", "Remote Desktop exposed; consider VPN or MFA"),
    "22": ("SSH", "Medium", "Check for weak ciphers and password auth"),
    "3306": ("MySQL", "Medium", "Database exposed; ensure auth and limit access"),
}

def analyze(parsed_results):
    issues = []
    for r in parsed_results:
        if r["port"] in RISKY_PORTS:
            name, severity, desc = RISKY_PORTS[r["port"]]
            issues.append({
                "host": r["host"],
                "hostname": r.get("hostname"),
                "port": r["port"],
                "service": r.get("service") or name,
                "severity": severity,
                "description": desc,
                "evidence": {
                    "product": r.get("product"),
                    "version": r.get("version"),
                    "state": r.get("state"),
                    "scripts": r.get("scripts")
                }
            })
        elif r.get("service") in ("http", "http-proxy", "http-alt") and r.get("state") == "open":
            sev = "Medium"
            desc = "HTTP service available; check for default pages, outdated server, directory listing."
            issues.append({
                "host": r["host"],
                "hostname": r.get("hostname"),
                "port": r["port"],
                "service": r.get("service"),
                "severity": sev,
                "description": desc,
                "evidence": {"product": r.get("product"), "version": r.get("version")}
            })

    severity_order = {"High": 0, "Medium": 1, "Low": 2}
    issues_sorted = sorted(issues, key=lambda x: (severity_order.get(x["severity"], 3), x["host"], x["port"]))
    return issues_sorted

