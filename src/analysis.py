"""Core Pandas analysis for Taobao user behavior and conversion funnels."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "data" / "cleaned_user_behavior.csv"


def load_data(input_path: Path = DEFAULT_INPUT) -> pd.DataFrame:
    df = pd.read_csv(input_path, parse_dates=["behavior_time"])
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def summarize_behavior_metrics(df: pd.DataFrame) -> dict[str, float | int]:
    behavior_counts = df["behavior_type"].value_counts()
    user_behavior = df.pivot_table(
        index="user_id",
        columns="behavior_type",
        values="item_id",
        aggfunc="count",
        fill_value=0,
    )

    for column in ["pv", "cart", "buy"]:
        if column not in user_behavior.columns:
            user_behavior[column] = 0

    pv_users = int((user_behavior["pv"] > 0).sum())
    cart_users = int((user_behavior["cart"] > 0).sum())
    buyers_after_view = int(((user_behavior["pv"] > 0) & (user_behavior["buy"] > 0)).sum())
    buyers_after_cart = int(((user_behavior["cart"] > 0) & (user_behavior["buy"] > 0)).sum())

    return {
        "total_behaviors": int(len(df)),
        "uv": int(df["user_id"].nunique()),
        "item_count": int(df["item_id"].nunique()),
        "category_count": int(df["category_id"].nunique()),
        "pv_count": int(behavior_counts.get("pv", 0)),
        "fav_count": int(behavior_counts.get("fav", 0)),
        "cart_count": int(behavior_counts.get("cart", 0)),
        "buy_count": int(behavior_counts.get("buy", 0)),
        "browse_to_purchase_user_rate": round(buyers_after_view / pv_users, 4) if pv_users else 0,
        "cart_to_purchase_user_rate": round(buyers_after_cart / cart_users, 4) if cart_users else 0,
    }


def user_level_funnel(df: pd.DataFrame) -> pd.DataFrame:
    """Build a user-level funnel based on whether a user ever reached each behavior."""
    user_flags = pd.crosstab(df["user_id"], df["behavior_type"]) > 0
    for column in ["pv", "fav", "cart", "buy"]:
        if column not in user_flags.columns:
            user_flags[column] = False

    steps = [
        ("01_viewed", user_flags["pv"]),
        ("02_favorited", user_flags["pv"] & user_flags["fav"]),
        ("03_added_to_cart", user_flags["pv"] & user_flags["cart"]),
        ("04_purchased", user_flags["pv"] & user_flags["buy"]),
    ]
    result = pd.DataFrame({"step": [step for step, _ in steps], "users": [int(mask.sum()) for _, mask in steps]})
    first_step_users = result.loc[0, "users"] if not result.empty else 0
    result["conversion_from_view"] = (
        result["users"].div(first_step_users).round(4) if first_step_users else 0
    )
    return result


def user_item_sequential_funnel(df: pd.DataFrame) -> dict[str, float | int]:
    """Calculate stricter user-item funnel rates that respect event order."""
    events = df[df["behavior_type"].isin(["pv", "fav", "cart", "buy"])].copy()
    first_times = events.pivot_table(
        index=["user_id", "item_id"],
        columns="behavior_type",
        values="behavior_time",
        aggfunc="min",
    )
    for column in ["pv", "fav", "cart", "buy"]:
        if column not in first_times.columns:
            first_times[column] = pd.NaT

    viewed = first_times["pv"].notna()
    favorited = first_times["fav"].notna()
    carted = first_times["cart"].notna()
    bought = first_times["buy"].notna()

    pv_to_buy = viewed & bought & (first_times["buy"] >= first_times["pv"])
    pv_to_cart = viewed & carted & (first_times["cart"] >= first_times["pv"])
    cart_to_buy = carted & bought & (first_times["buy"] >= first_times["cart"])
    fav_to_buy = favorited & bought & (first_times["buy"] >= first_times["fav"])

    viewed_pairs = int(viewed.sum())
    carted_pairs = int(carted.sum())
    favorited_pairs = int(favorited.sum())

    return {
        "user_item_pairs": int(len(first_times)),
        "viewed_pairs": viewed_pairs,
        "carted_pairs": carted_pairs,
        "favorited_pairs": favorited_pairs,
        "bought_pairs": int(bought.sum()),
        "pv_to_cart_pairs": int(pv_to_cart.sum()),
        "pv_to_buy_pairs": int(pv_to_buy.sum()),
        "cart_to_buy_pairs": int(cart_to_buy.sum()),
        "fav_to_buy_pairs": int(fav_to_buy.sum()),
        "pv_to_cart_pair_rate": round(int(pv_to_cart.sum()) / viewed_pairs, 4) if viewed_pairs else 0,
        "pv_to_buy_pair_rate": round(int(pv_to_buy.sum()) / viewed_pairs, 4) if viewed_pairs else 0,
        "cart_to_buy_pair_rate": round(int(cart_to_buy.sum()) / carted_pairs, 4) if carted_pairs else 0,
        "fav_to_buy_pair_rate": round(int(fav_to_buy.sum()) / favorited_pairs, 4) if favorited_pairs else 0,
    }


def behavior_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["behavior_type"].value_counts().rename_axis("behavior_type").reset_index(name="behavior_count")
    counts["behavior_share"] = (counts["behavior_count"] / counts["behavior_count"].sum()).round(4)
    return counts


def daily_active_users(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("date")["user_id"].nunique().reset_index(name="dau")


def daily_purchase_trend(df: pd.DataFrame) -> pd.DataFrame:
    buy_df = df[df["behavior_type"] == "buy"]
    return (
        buy_df.groupby("date")
        .agg(purchase_count=("behavior_type", "size"), purchase_users=("user_id", "nunique"))
        .reset_index()
    )


def hourly_activity(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["hour", "behavior_type"]).size().reset_index(name="behavior_count")


def top_categories_by_purchase(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    buy_df = df[df["behavior_type"] == "buy"]
    return (
        buy_df.groupby("category_id")
        .agg(purchase_count=("behavior_type", "size"), buyer_count=("user_id", "nunique"))
        .sort_values(["purchase_count", "buyer_count"], ascending=False)
        .head(top_n)
        .reset_index()
    )


def category_conversion_analysis(df: pd.DataFrame, top_n: int = 20, min_pv: int = 30) -> pd.DataFrame:
    """Summarize category-level behavior volume and conversion efficiency."""
    category_behavior = (
        df.pivot_table(
            index="category_id",
            columns="behavior_type",
            values="user_id",
            aggfunc="count",
            fill_value=0,
        )
        .rename_axis(None, axis=1)
        .reset_index()
    )
    for column in ["pv", "fav", "cart", "buy"]:
        if column not in category_behavior.columns:
            category_behavior[column] = 0

    category_behavior = category_behavior.rename(
        columns={
            "pv": "pv_count",
            "fav": "fav_count",
            "cart": "cart_count",
            "buy": "buy_count",
        }
    )
    category_behavior["browse_to_buy_rate"] = (
        category_behavior["buy_count"] / category_behavior["pv_count"].replace(0, float("nan"))
    ).fillna(0.0).round(4)
    category_behavior["cart_to_buy_rate"] = (
        category_behavior["buy_count"] / category_behavior["cart_count"].replace(0, float("nan"))
    ).fillna(0.0).round(4)

    return (
        category_behavior[category_behavior["pv_count"] >= min_pv]
        .sort_values(["buy_count", "browse_to_buy_rate"], ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def repurchase_analysis(df: pd.DataFrame) -> dict[str, float | int]:
    user_buy_counts = df[df["behavior_type"] == "buy"].groupby("user_id").size()
    total_buyers = int(user_buy_counts.shape[0])
    repurchase_users = int((user_buy_counts >= 2).sum())
    return {
        "total_buyers": total_buyers,
        "repurchase_users": repurchase_users,
        "repurchase_rate": round(repurchase_users / total_buyers, 4) if total_buyers else 0,
    }


def cart_without_purchase_users(df: pd.DataFrame) -> pd.DataFrame:
    user_flags = df.pivot_table(
        index="user_id",
        columns="behavior_type",
        values="item_id",
        aggfunc="count",
        fill_value=0,
    )
    user_flags.columns.name = None
    for column in ["cart", "buy"]:
        if column not in user_flags.columns:
            user_flags[column] = 0

    result = user_flags[(user_flags["cart"] > 0) & (user_flags["buy"] == 0)].reset_index()
    return result[["user_id", "cart"]].rename(columns={"cart": "cart_count"})


def high_value_users(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    buy_df = df[df["behavior_type"] == "buy"]
    if buy_df.empty:
        return pd.DataFrame(columns=["user_id", "purchase_count", "distinct_items_bought", "active_days", "value_score"])

    user_purchase = buy_df.groupby("user_id").agg(
        purchase_count=("behavior_type", "size"),
        distinct_items_bought=("item_id", "nunique"),
        distinct_categories_bought=("category_id", "nunique"),
    )
    user_active_days = df.groupby("user_id")["date"].nunique().rename("active_days")
    result = user_purchase.join(user_active_days, how="left").fillna(0)
    result["value_score"] = (
        result["purchase_count"] * 5
        + result["distinct_items_bought"] * 2
        + result["distinct_categories_bought"]
        + result["active_days"]
    )
    return result.sort_values(["value_score", "purchase_count"], ascending=False).head(top_n).reset_index()


def user_segmentation(df: pd.DataFrame) -> pd.DataFrame:
    """Group users by behavior depth and summarize value indicators."""
    user_behavior = (
        df.pivot_table(
            index="user_id",
            columns="behavior_type",
            values="item_id",
            aggfunc="count",
            fill_value=0,
        )
        .rename_axis(None, axis=1)
        .reset_index()
    )
    for column in ["pv", "fav", "cart", "buy"]:
        if column not in user_behavior.columns:
            user_behavior[column] = 0

    active_days = df.groupby("user_id")["date"].nunique().rename("active_days").reset_index()
    user_behavior = user_behavior.merge(active_days, on="user_id", how="left")
    user_behavior["purchase_segment"] = pd.cut(
        user_behavior["buy"],
        bins=[-1, 0, 1, 3, float("inf")],
        labels=["no_purchase", "one_purchase", "two_to_three", "four_plus"],
    )
    user_behavior["activity_segment"] = pd.cut(
        user_behavior["active_days"],
        bins=[0, 2, 5, float("inf")],
        labels=["low_active", "medium_active", "high_active"],
        include_lowest=True,
    )
    user_behavior["behavior_depth"] = "browse_only"
    user_behavior.loc[user_behavior["fav"] > 0, "behavior_depth"] = "favorited"
    user_behavior.loc[user_behavior["cart"] > 0, "behavior_depth"] = "added_to_cart"
    user_behavior.loc[user_behavior["buy"] > 0, "behavior_depth"] = "purchased"

    return (
        user_behavior.groupby(["behavior_depth", "purchase_segment"], observed=True)
        .agg(
            users=("user_id", "nunique"),
            avg_active_days=("active_days", "mean"),
            total_purchases=("buy", "sum"),
            avg_purchase_count=("buy", "mean"),
            avg_cart_count=("cart", "mean"),
        )
        .reset_index()
        .sort_values(["behavior_depth", "purchase_segment"])
    )


def print_section(title: str, value: object) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    print(value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Taobao behavior analysis.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Cleaned CSV path.")
    args = parser.parse_args()

    df = load_data(args.input)
    print_section("Core Metrics", pd.Series(summarize_behavior_metrics(df)))
    print_section("Behavior Type Distribution", behavior_type_distribution(df))
    print_section("User-Level Funnel", user_level_funnel(df))
    print_section("User-Item Sequential Funnel", pd.Series(user_item_sequential_funnel(df)))
    print_section("Daily Active Users", daily_active_users(df))
    print_section("Daily Purchase Trend", daily_purchase_trend(df))
    print_section("Hourly Activity", hourly_activity(df).head(24))
    print_section("Top 10 Categories by Purchase", top_categories_by_purchase(df))
    print_section("Category Conversion Analysis", category_conversion_analysis(df, top_n=10))
    print_section("Repurchase Analysis", pd.Series(repurchase_analysis(df)))
    print_section("Cart Without Purchase Users", cart_without_purchase_users(df).head(20))
    print_section("High Value Users", high_value_users(df))
    print_section("User Segmentation", user_segmentation(df))


if __name__ == "__main__":
    main()
