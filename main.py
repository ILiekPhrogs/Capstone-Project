import argparse
import sys
from scanners.nmap_runner import run_nmap_scan
from scanners.parser_nmap import parse_nmap_xml
from analysis.analyzer import analyze
from reporting.ai_helper import summarize_issues
from reporting.generator import generate_report
from utils import ensure_nmap_installed

def main():
    parser = argparse.ArgumentParser(description="Security Scan Assistant")
    parser.add_argument("--scan", help="Target to scan with Nmap")
    parser.add_argument("--file", help="Parse existing scan XML file")
    parser.add_argument("--nmap-args", help="Extra nmap args e.g. '-p 1-65535 -T4'", default="")
    parser.add_argument("--output", help="Report output filename (pdf or txt)", default="report.pdf")
    args = parser.parse_args()

# Safety check
    ensure_nmap_installed()

    if args.scan and args.file:
        print("Provide only one of --scan or --file", file=sys.stderr)
        sys.exit(1)

    if args.scan:
        xml_file = run_nmap_scan(args.scan, extra_args=args.nmap_args)
    elif args.file:
        xml_file = args.file
    else:
        parser.print_help()
        return

    results = parse_nmap_xml(xml_file)
    issues = analyze(results)
    ai_report = summarize_issues(issues)
    report_file = generate_report(ai_report, results, output_file=args.output)

    print(f"Report saved to {report_file}")

if __name__ == "__main__":
    main()
