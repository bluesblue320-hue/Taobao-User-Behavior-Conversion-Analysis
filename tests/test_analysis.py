from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from analysis import summarize_behavior_metrics, user_item_sequential_funnel


def test_summarize_behavior_metrics_user_level_rates():
    df = pd.DataFrame(
        [
            [1, 10, 100, "pv"],
            [1, 10, 100, "cart"],
            [1, 10, 100, "buy"],
            [2, 20, 200, "pv"],
            [2, 20, 200, "cart"],
        ],
        columns=["user_id", "item_id", "category_id", "behavior_type"],
    )

    metrics = summarize_behavior_metrics(df)

    assert metrics["total_behaviors"] == 5
    assert metrics["uv"] == 2
    assert metrics["pv_count"] == 2
    assert metrics["cart_count"] == 2
    assert metrics["buy_count"] == 1
    assert metrics["browse_to_purchase_user_rate"] == 0.5
    assert metrics["cart_to_purchase_user_rate"] == 0.5


def test_user_item_sequential_funnel_requires_event_order():
    df = pd.DataFrame(
        [
            [1, 10, 100, "pv", "2017-11-25 10:00:00"],
            [1, 10, 100, "cart", "2017-11-25 10:05:00"],
            [1, 10, 100, "buy", "2017-11-25 10:10:00"],
            [2, 20, 200, "buy", "2017-11-25 11:00:00"],
            [2, 20, 200, "pv", "2017-11-25 11:05:00"],
            [3, 30, 300, "buy", "2017-11-25 12:00:00"],
            [3, 30, 300, "cart", "2017-11-25 12:05:00"],
        ],
        columns=["user_id", "item_id", "category_id", "behavior_type", "behavior_time"],
    )
    df["behavior_time"] = pd.to_datetime(df["behavior_time"])

    funnel = user_item_sequential_funnel(df)

    assert funnel["viewed_pairs"] == 2
    assert funnel["carted_pairs"] == 2
    assert funnel["bought_pairs"] == 3
    assert funnel["pv_to_buy_pairs"] == 1
    assert funnel["cart_to_buy_pairs"] == 1
    assert funnel["pv_to_buy_pair_rate"] == 0.5
    assert funnel["cart_to_buy_pair_rate"] == 0.5
