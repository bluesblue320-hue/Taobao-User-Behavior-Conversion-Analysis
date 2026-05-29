"""Generate a small Taobao-style user behavior sample dataset.

The public Tianchi UserBehavior.csv file is large. This script creates a
deterministic, resume-friendly sample with the same columns so the project can
run end-to-end before the full dataset is downloaded.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw_user_behavior_sample.csv"
BASE_TIME = pd.Timestamp("2017-11-25 00:00:00")
END_TIME = pd.Timestamp("2017-12-03 23:59:59")


def _random_timestamp(rng: random.Random) -> int:
    seconds = int((END_TIME - BASE_TIME).total_seconds())
    return int((BASE_TIME + pd.Timedelta(seconds=rng.randint(0, seconds))).timestamp())


def generate_sample(rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Create a Taobao-style behavior log with light funnel structure."""
    rng = random.Random(seed)
    records: list[dict[str, int | str]] = []

    user_ids = list(range(100001, 100401))
    item_ids = list(range(200001, 201201))
    category_ids = list(range(3001, 3061))
    item_to_category = {item: rng.choice(category_ids) for item in item_ids}

    while len(records) < rows:
        user_id = rng.choice(user_ids)
        item_id = rng.choice(item_ids)
        category_id = item_to_category[item_id]
        start_ts = _random_timestamp(rng)

        session_events = ["pv"]
        if rng.random() < 0.18:
            session_events.append("fav")
        if rng.random() < 0.26:
            session_events.append("cart")
        if "cart" in session_events and rng.random() < 0.34:
            session_events.append("buy")
        elif rng.random() < 0.035:
            session_events.append("buy")

        for step, behavior_type in enumerate(session_events):
            records.append(
                {
                    "user_id": user_id,
                    "item_id": item_id,
                    "category_id": category_id,
                    "behavior_type": behavior_type,
                    "timestamp": start_ts + step * rng.randint(60, 1800),
                }
            )
            if len(records) >= rows:
                break

    df = pd.DataFrame(records)
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sample Taobao behavior data.")
    parser.add_argument("--rows", type=int, default=5000, help="Number of rows to generate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output CSV path.")
    args = parser.parse_args()

    df = generate_sample(rows=args.rows, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Generated {len(df):,} rows at {args.output}")


if __name__ == "__main__":
    main()
