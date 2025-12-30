from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    root: Path
    data: Path
    raw: Path
    processed: Path
    models: Path
    reports: Path
    metrics: Path

    @classmethod
    def from_repo_root(cls) -> "Paths":
        root = Path(__file__).resolve().parents[2]
        data = root / "data"

        return cls(
            root=root,
            data=data,
            raw=data / "raw",
            processed=data / "processed",
            models=root / "models",
            reports=root / "reports",
            metrics=root / "metrics",
        )
