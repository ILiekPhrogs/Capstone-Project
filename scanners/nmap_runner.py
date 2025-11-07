import subprocess
import shutil
import tempfile
import datetime
from pathlib import Path

def run_nmap_scan(target, output_file=None, extra_args=""):
   #run nmap as if in terminal on targetted network
 if not shutil.which("nmap"):
      raise FileNotFoundError("nmap not found in PATH. Please install nmap.")

 if output_file is None:
      ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
      output_file = f"nmap_scan_{ts}.xml"
    # build command safely
      cmd = ["nmap", "-sV", "-oX", output_file]
 if extra_args:
   cmd += extra_args.split()
   cmd.append(target)

 try:
   subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 except subprocess.CalledProcessError as e:
   raise RuntimeError(f"Nmap failed: {e.stderr.decode() or e}") from e

 return Path(output_file).resolve()