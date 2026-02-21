from pathlib import Path
import json
from datetime import datetime

def build_report(parsed: dict, validation: dict, output_dir: str) -> str:
    out = Path(output_dir) / "report.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    summary = validation.get("summary", {})
    lines = []
    lines.append("# Migration Report")
    lines.append("")
    lines.append(f"- Generated: {datetime.utcnow().isoformat()}Z")
    lines.append("")
    lines.append("## Summary")
    lines.append(f"- Objects parsed: {len(parsed.get('objects', []))}")
    lines.append(f"- Queries parsed: {len(parsed.get('queries', []))}")
    lines.append(f"- Validation status: {summary.get('status', 'unknown')}")
    lines.append("")
    lines.append("## Validation")
    lines.append("```json")
    lines.append(json.dumps(validation, indent=2))
    lines.append("```")
    out.write_text("\\n".join(lines), encoding="utf-8")
    return str(out)