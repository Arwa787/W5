from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    path.write_text(json_text, encoding="utf-8")


def md_header(report: dict) -> str:
    lines = []
    lines.append("# CSV Profile Report")
    lines.append("")
    if report.get("source"):
        lines.append(f"**Source:** `{report['source']}`")
        lines.append("")
    return "\n".join(lines)


def write_markdown(report: dict, path: str | Path = None) -> str:
    lines = []
    
    lines.append(md_header(report))
    
    summary = report.get("summary", {})
    n_rows = summary.get("n_rows", 0)
    n_cols = summary.get("n_cols", 0)
    
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Rows:** {n_rows}")
    lines.append(f"- **Columns:** {n_cols}")
    lines.append("")
    
    lines.append("## Column Overview")
    lines.append("")
    lines.append("| Column Name | Type | Missing % | Unique |")
    lines.append("|-------------|------|-----------|--------|")
    
    columns = report.get("columns", {})
    
    if isinstance(columns, dict):
        for col_name, col_report in columns.items():
            col_type = col_report.get("type", "unknown")
            missing = col_report.get("missing", 0)
            unique = col_report.get("unique", 0)
            missing_pct = (missing / n_rows * 100) if n_rows else 0.0
            lines.append(f"| {col_name} | {col_type} | {missing_pct:.1f}% | {unique} |")
    elif isinstance(columns, list):
        for col_name in columns:
            lines.append(f"| {col_name} | - | - | - |")
    
    lines.append("")
    
    lines.append("## Column Details")
    lines.append("")
    
    if isinstance(columns, dict):
        for col_name, col_report in columns.items():
            col_type = col_report.get("type", "unknown")
            lines.append(f"### {col_name}")
            lines.append("")
            lines.append(f"**Type:** {col_type}")
            lines.append("")
            
            if col_type == "number":
                min_val = col_report.get("min")
                max_val = col_report.get("max")
                mean_val = col_report.get("mean")
                
                lines.append(f"- **Min:** {min_val}")
                lines.append(f"- **Max:** {max_val}")
                lines.append(f"- **Mean:** {mean_val:.2f}" if mean_val is not None else "- **Mean:** N/A")
                lines.append("")
                
            elif col_type == "text":
                top = col_report.get("top", [])
                if top:
                    lines.append("**Top values:**")
                    lines.append("")
                    for value, count in top:
                        lines.append(f"- `{value}`: {count}")
                    lines.append("")
    
    markdown_text = "\n".join(lines)
    
    if path is not None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown_text, encoding="utf-8")
    
    return markdown_text


def render_markdown(report: dict) -> str:
    lines: list[str] = []

    lines.append(f"# CSV Profiling Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")

    lines.append("## Summary\n")
    
    summary = report.get("summary", {})
    n_rows = summary.get("n_rows", report.get("n_rows", 0))
    n_cols = summary.get("n_cols", report.get("n_cols", 0))
    
    lines.append(f"- Rows: **{n_rows}**")
    lines.append(f"- Columns: **{n_cols}**\n")

    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")
    
    columns = report.get("columns", {})
    
    if isinstance(columns, dict):
        for col_name, col_report in columns.items():
            col_type = col_report.get("type", "unknown")
            missing = col_report.get("missing", 0)
            unique = col_report.get("unique", 0)
            missing_pct = (missing / n_rows * 100) if n_rows else 0.0
            lines.append(f"| {col_name} | {col_type} | {missing} | {missing_pct:.1f}% | {unique} |")
    elif isinstance(columns, list):
        for col_name in columns:
            lines.append(f"| {col_name} | - | - | - | - |")
    
    lines.append("\n## Notes\n")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")

    return "\n".join(lines)