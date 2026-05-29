"""Prepare a GitHub-friendly real sample from the full Tianchi UserBehavior.csv.

The full public dataset is too large for GitHub. After downloading the official
UserBehavior.csv manually, run this script to extract a real, same-schema sample
that replaces the generated synthetic sample used for the MVP.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "UserBehavior.csv"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw_user_behavior_sample.csv"
REQUIRED_COLUMNS = ["user_id", "item_id", "category_id", "behavior_type", "timestamp"]
VALID_BEHAVIORS = {"pv", "fav", "cart", "buy"}


def _iter_csv_chunks(input_path: Path, chunksize: int):
    """Yield CSV chunks from a plain CSV or a zip containing UserBehavior.csv."""
    if input_path.suffix.lower() == ".zip":
        with ZipFile(input_path) as zip_file:
            csv_names = [name for name in zip_file.namelist() if name.lower().endswith(".csv")]
            if not csv_names:
                raise ValueError(f"No CSV file found inside {input_path}")

            preferred = [name for name in csv_names if Path(name).name.lower() == "userbehavior.csv"]
            csv_name = preferred[0] if preferred else csv_names[0]
            with zip_file.open(csv_name) as csv_file:
                yield from pd.read_csv(csv_file, header=None, names=REQUIRED_COLUMNS, chunksize=chunksize)
        return

    yield from pd.read_csv(input_path, header=None, names=REQUIRED_COLUMNS, chunksize=chunksize)


def prepare_real_sample(
    input_path: Path = DEFAULT_INPUT,
    output_path: Path = DEFAULT_OUTPUT,
    rows: int = 100000,
    chunksize: int = 500000,
    sample_mode: str = "first",
    random_state: int = 42,
) -> pd.DataFrame:
    """Extract a valid real sample from official headerless UserBehavior.csv."""
    if not input_path.exists():
        raise FileNotFoundError(
            f"Real dataset not found: {input_path}. "
            "Download UserBehavior.csv or UserBehavior.csv.zip from Tianchi/Kaggle first and place it under data/."
        )

    collected: list[pd.DataFrame] = []
    random_sample: pd.DataFrame | None = None
    rng = np.random.default_rng(random_state)
    total_rows = 0

    for chunk in _iter_csv_chunks(input_path, chunksize):
        chunk = chunk.dropna(subset=REQUIRED_COLUMNS)
        chunk["behavior_type"] = chunk["behavior_type"].astype(str).str.lower().str.strip()
        chunk = chunk[chunk["behavior_type"].isin(VALID_BEHAVIORS)]
        total_rows += len(chunk)

        if sample_mode == "first":
            collected.append(chunk)
        elif sample_mode == "random":
            chunk = chunk.copy()
            chunk["_sample_key"] = rng.random(len(chunk))
            random_sample = chunk if random_sample is None else pd.concat([random_sample, chunk], ignore_index=True)
            random_sample = random_sample.nsmallest(rows, "_sample_key")
        else:
            raise ValueError("sample_mode must be 'first' or 'random'.")

        if sample_mode == "first" and total_rows >= rows:
            break

    if sample_mode == "first":
        if not collected:
            raise ValueError("No valid rows were found in the source file.")
        sample = pd.concat(collected, ignore_index=True).head(rows)
    else:
        if random_sample is None or random_sample.empty:
            raise ValueError("No valid rows were found in the source file.")
        sample = random_sample.drop(columns=["_sample_key"]).reset_index(drop=True)

    if sample.empty:
        raise ValueError("No valid rows were found in the source file.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sample.to_csv(output_path, index=False)

    print(f"Prepared {len(sample):,} real rows at {output_path}")
    print("Next: python src/data_cleaning.py --input data/raw_user_behavior_sample.csv --output data/cleaned_user_behavior.csv")
    return sample


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract a real sample from Tianchi UserBehavior.csv.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to official UserBehavior.csv.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output sample CSV path.")
    parser.add_argument("--rows", type=int, default=100000, help="Number of real rows to keep.")
    parser.add_argument("--chunksize", type=int, default=500000, help="Rows per read chunk.")
    parser.add_argument(
        "--sample-mode",
        choices=["first", "random"],
        default="first",
        help="Use first rows for speed or random rows for a less biased sample.",
    )
    parser.add_argument("--random-state", type=int, default=42, help="Random seed used by --sample-mode random.")
    args = parser.parse_args()

    prepare_real_sample(
        input_path=args.input,
        output_path=args.output,
        rows=args.rows,
        chunksize=args.chunksize,
        sample_mode=args.sample_mode,
        random_state=args.random_state,
    )


if __name__ == "__main__":
    main()
