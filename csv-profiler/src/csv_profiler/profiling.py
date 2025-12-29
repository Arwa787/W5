from __future__ import annotations


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


MISSING = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().casefold() in MISSING

def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    return [row.get(col, "") for row in rows]

def numeric_stats(values: list[str]) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums: list[float] = []
    for v in usable:
        x = try_float(v)
        if x is None:
            raise ValueError(f"Non-numeric value found: {v!r}")
        nums.append(x)

    count = len(nums)
    unique = len(set(nums))
    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min(nums) if nums else None,
        "max": max(nums) if nums else None,
        "mean": (sum(nums) / count) if count else None,
    }

def text_stats(values: list[str], top_k: int = 5) -> dict:
    total_count = len(values)
    
    non_missing = [v for v in values if not is_missing(v)]
    
    missing_count = total_count - len(non_missing)
    unique_count = len(set(non_missing))
    
    counts: dict[str, int] = {}
    for v in non_missing:
        counts[v] = counts.get(v, 0) + 1
    
    top = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    
    return {
        "count": total_count,
        "missing": missing_count,
        "unique": unique_count,
        "top": top
    }


def basic_profile(rows: list[dict[str, str]], source: str = None) -> dict:
    if not rows:
        return {
            "source": source,
            "summary": {
                "n_rows": 0,
                "n_cols": 0
            },
            "columns": {}
        }
    
    column_names = list(rows[0].keys())
    n_rows = len(rows)
    n_cols = len(column_names)
    
    columns = {}
    
    for col in column_names:
        values = column_values(rows, col)
        col_type = infer_type(values)
        
        if col_type == "number":
            columns[col] = {
                "type": "number",
                **numeric_stats(values)
            }
        else:
            columns[col] = {
                "type": "text",
                **text_stats(values)
            }
    
    return {
        "source": source,
        "summary": {
            "n_rows": n_rows,
            "n_cols": n_cols
        },
        "columns": columns
    }

rows_example = [
    {"age": "25",   "city": "Riyadh"},
    {"age": "30",   "city": "Jeddah"},
    {"age": None,   "city": "Dammam"},
    {"age": "22.5", "city": ""},
    {"age": "NA",   "city": "Mecca"},
    {"age": "40",   "city": None},
]





def is_missing(value: str | None) -> bool:
    if value is None:
        return True
    cleaned = value.strip().casefold()
    return cleaned in {"", "na", "n/a", "null", "none", "nan"}

def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

from collections import Counter
def profile_rows(rows: list[dict[str, str]]) -> dict:
    n_rows, columns = len(rows), list(rows[0].keys())
    col_profiles = []
    for col in columns:
        values = [r.get(col, "") for r in rows]
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        inferred = infer_type(values)
        unique = len(set(usable))
        profile = {
            "name": col,
            "type": inferred,
            "missing": missing,
            "missing_pct": 100.0 * missing / n_rows if n_rows else 0.0,
            "unique": unique,
        }
        if inferred == "number":
            nums = [try_float(v) for v in usable]
            nums = [x for x in nums if x is not None]
            if nums:
                profile.update({"min": min(nums), "max": max(nums), "mean": sum(nums) / len(nums)})
        col_profiles.append(profile)
    return {"n_rows": n_rows, "n_cols": len(columns), "columns": col_profiles}
