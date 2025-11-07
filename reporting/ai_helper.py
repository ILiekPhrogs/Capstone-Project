import time
import json
from typing import List
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Convert structured scan findings into a "
    "clear, prioritized vulnerability report for technical audiences and an executive summary for non-technical stakeholders. "
    "For each finding include: summary, technical details/evidence, risk level, and remediation steps."
)

def _build_prompt_chunk(issues_chunk):
    content = {
        "type": "issues_chunk",
        "issues": issues_chunk
    }
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        "Input (JSON):\n"
        f"{json.dumps(content, indent=2)}\n\n"
        "Produce:\n"
        "1) Short executive summary (2-4 sentences)\n"
        "2) For each finding: Title, Severity, Evidence, Detailed description, Remediation steps\n"
        "3) Final prioritized checklist\n"
    )
    return prompt

def summarize_issues(issues: List[dict], max_chunk_size=30):
   
    if not issues:
        return "No immediate risky issues detected by the automated scanner."

    # chunking
    chunks = [issues[i:i + max_chunk_size] for i in range(0, len(issues), max_chunk_size)]
    reports = []
    for i, chunk in enumerate(chunks):
        prompt = _build_prompt_chunk(chunk)
        # retry loop
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                )
                text = response.choices[0].message.content
                reports.append(text)
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(1 + attempt * 2)
                    continue
                raise

    # simple concatenation with section headers
    final_report = "# AI-Generated Vulnerability Summary\n\n"
    for idx, rpt in enumerate(reports, start=1):
        final_report += f"## Chunk {idx}\n\n{rpt}\n\n"
    return final_report