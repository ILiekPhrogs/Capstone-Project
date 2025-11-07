import shutil
import sys

def ensure_nmap_installed():
    if shutil.which("nmap") is None:
        print("nmap not found in PATH. Install nmap and retry.", file=sys.stderr)
        sys.exit(2)
