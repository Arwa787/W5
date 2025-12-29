import json
import time
import typer
from pathlib import Path

from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import basic_profile
from csv_profiler.render import render_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
):
    start_time = time.time()
    
    typer.echo(f"Reading CSV: {input_path}")
    rows = read_csv_rows(input_path)
    
    if not rows:
        typer.echo("Error: CSV file is empty", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"Profiling {len(rows)} rows...")
    report = basic_profile(rows, source=str(input_path))
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = out_dir / f"{report_name}.json"
    md_path = out_dir / f"{report_name}.md"
    
    typer.echo(f"Writing JSON: {json_path}")
    json_text = json.dumps(report, indent=2, ensure_ascii=False)
    json_path.write_text(json_text, encoding="utf-8")
    
    typer.echo(f"Writing Markdown: {md_path}")
    md_text = render_markdown(report)
    md_path.write_text(md_text, encoding="utf-8")
    
    elapsed = time.time() - start_time
    typer.echo(f"Done in {elapsed:.2f}s")
    
    if preview:
        summary = report.get("summary", {})
        n_rows = summary.get("n_rows", 0)
        n_cols = summary.get("n_cols", 0)
        typer.echo("\n=== Preview ===")
        typer.echo(f"Rows: {n_rows}")
        typer.echo(f"Columns: {n_cols}")
        typer.echo(f"Columns: {list(report.get('columns', {}).keys())}")

if __name__ == "__main__":
    app()