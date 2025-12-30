import typer
from pathlib import Path

from ml_baseline.sample_data import make_sample_feature_table

app = typer.Typer(help="ML Baseline CLI")

@app.command()
def make_sample_data(
    n_users: int = 50,
    seed: int = 42,
):
    """Generate sample feature data and save it to data/processed."""
    
    path = make_sample_feature_table(
        n_users=n_users,
        seed=seed,
    )
    
    typer.echo(f"Sample data written to: {path}")

if __name__ == "__main__":
    app()
