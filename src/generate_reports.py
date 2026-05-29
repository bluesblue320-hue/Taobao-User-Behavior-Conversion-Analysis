"""Generate markdown reports and chart images from the cleaned behavior dataset."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from analysis import (
    behavior_type_distribution,
    cart_without_purchase_users,
    category_conversion_analysis,
    daily_active_users,
    daily_purchase_trend,
    high_value_users,
    hourly_activity,
    load_data,
    repurchase_analysis,
    summarize_behavior_metrics,
    top_categories_by_purchase,
    user_item_sequential_funnel,
    user_level_funnel,
    user_segmentation,
)
from data_cleaning import DEFAULT_TIMEZONE, REQUIRED_COLUMNS, VALID_BEHAVIORS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw_user_behavior_sample.csv"
CLEANED_PATH = PROJECT_ROOT / "data" / "cleaned_user_behavior.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DASHBOARD_DATA_PATH = REPORTS_DIR / "dashboard_data.json"


def pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:,.4f}".rstrip("0").rstrip(".")
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_无数据。_"

    display_df = df.copy()
    for column in display_df.columns:
        if pd.api.types.is_float_dtype(display_df[column]):
            display_df[column] = display_df[column].map(fmt)
        elif pd.api.types.is_integer_dtype(display_df[column]):
            display_df[column] = display_df[column].map(lambda x: f"{int(x):,}")

    headers = [str(column) for column in display_df.columns]
    rows = [[str(value) for value in row] for row in display_df.to_numpy()]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def data_quality_summary(raw_path: Path, cleaned_df: pd.DataFrame) -> dict[str, object]:
    raw_df = pd.read_csv(raw_path)
    normalized_behavior = raw_df["behavior_type"].astype(str).str.lower().str.strip()
    numeric_df = raw_df.copy()
    for column in ["user_id", "item_id", "category_id", "timestamp"]:
        numeric_df[column] = pd.to_numeric(numeric_df[column], errors="coerce")

    raw_time = (
        pd.to_datetime(numeric_df["timestamp"], unit="s", utc=True, errors="coerce")
        .dt.tz_convert(DEFAULT_TIMEZONE)
        .dt.tz_localize(None)
    )
    start_ts = pd.Timestamp("2017-11-25")
    end_ts = pd.Timestamp("2017-12-04")
    valid_required = raw_df[REQUIRED_COLUMNS].notna().all(axis=1)
    valid_numeric = numeric_df[["user_id", "item_id", "category_id", "timestamp"]].notna().all(axis=1)
    valid_behavior = normalized_behavior.isin(VALID_BEHAVIORS)
    valid_time = raw_time.notna()
    abnormal_time = valid_required & valid_numeric & valid_behavior & valid_time & ~(
        (raw_time >= start_ts) & (raw_time < end_ts)
    )

    return {
        "raw_rows": int(len(raw_df)),
        "duplicate_rows": int(raw_df.duplicated().sum()),
        "missing_required_rows": int((~valid_required).sum()),
        "non_numeric_id_or_timestamp_rows": int((valid_required & ~valid_numeric).sum()),
        "invalid_behavior_rows": int((valid_required & valid_numeric & ~valid_behavior).sum()),
        "abnormal_time_rows": int(abnormal_time.sum()),
        "clean_rows": int(len(cleaned_df)),
        "removed_rows": int(len(raw_df) - len(cleaned_df)),
        "raw_date_min": str(raw_time.min()),
        "raw_date_max": str(raw_time.max()),
        "clean_date_min": str(cleaned_df["behavior_time"].min()),
        "clean_date_max": str(cleaned_df["behavior_time"].max()),
    }


def save_figures(df: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False

    behavior_dist = behavior_type_distribution(df)
    plt.figure(figsize=(8, 4.5))
    sns.barplot(data=behavior_dist, x="behavior_type", y="behavior_count", color="#2F80ED")
    plt.title("行为类型分布")
    plt.xlabel("行为类型")
    plt.ylabel("行为次数")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "behavior_distribution.png", dpi=180)
    plt.close()

    dau = daily_active_users(df)
    purchases = daily_purchase_trend(df)
    trend = dau.merge(purchases, on="date", how="left").fillna(0)
    plt.figure(figsize=(9, 4.8))
    sns.lineplot(data=trend, x="date", y="dau", marker="o", label="日活用户")
    sns.lineplot(data=trend, x="date", y="purchase_count", marker="o", label="购买次数")
    plt.title("每日活跃用户与购买趋势")
    plt.xlabel("日期")
    plt.ylabel("数量")
    plt.xticks(rotation=35)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "daily_trends.png", dpi=180)
    plt.close()

    hourly = hourly_activity(df)
    hourly_pivot = hourly.pivot_table(index="behavior_type", columns="hour", values="behavior_count", fill_value=0)
    plt.figure(figsize=(11, 3.8))
    sns.heatmap(hourly_pivot, cmap="YlGnBu")
    plt.title("小时行为热力图")
    plt.xlabel(f"小时（{DEFAULT_TIMEZONE}）")
    plt.ylabel("行为类型")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "hourly_behavior_heatmap.png", dpi=180)
    plt.close()

    top_categories = top_categories_by_purchase(df, top_n=10).sort_values("purchase_count")
    plt.figure(figsize=(8, 5))
    sns.barplot(data=top_categories, x="purchase_count", y=top_categories["category_id"].astype(str), color="#27AE60")
    plt.title("购买次数 Top 10 品类")
    plt.xlabel("购买次数")
    plt.ylabel("品类 ID")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "top_categories_purchase.png", dpi=180)
    plt.close()


def write_data_quality_report(summary: dict[str, object], raw_behavior: pd.DataFrame, cleaned_df: pd.DataFrame) -> None:
    quality_table = pd.DataFrame(
        [
            ["原始行数", summary["raw_rows"]],
            ["重复行数", summary["duplicate_rows"]],
            ["必要字段缺失行数", summary["missing_required_rows"]],
            ["ID 或时间戳非数值行数", summary["non_numeric_id_or_timestamp_rows"]],
            ["非法行为类型行数", summary["invalid_behavior_rows"]],
            ["分析窗口外行数", summary["abnormal_time_rows"]],
            ["清洗后行数", summary["clean_rows"]],
            ["剔除行数", summary["removed_rows"]],
        ],
        columns=["检查项", "数值"],
    )
    raw_dist = raw_behavior["behavior_type"].value_counts().rename_axis("behavior_type").reset_index(name="raw_count")
    clean_dist = (
        cleaned_df["behavior_type"].value_counts().rename_axis("behavior_type").reset_index(name="clean_count")
    )
    dist = raw_dist.merge(clean_dist, on="behavior_type", how="outer").fillna(0)
    dist[["raw_count", "clean_count"]] = dist[["raw_count", "clean_count"]].astype(int)
    dist = dist.rename(
        columns={
            "behavior_type": "行为类型",
            "raw_count": "原始行数",
            "clean_count": "清洗后行数",
        }
    )

    content = f"""# 数据质量报告

业务分析使用的时区：`{DEFAULT_TIMEZONE}`。

## 清洗概览

{markdown_table(quality_table)}

## 时间范围

| 数据集 | 最早时间 | 最晚时间 |
| --- | --- | --- |
| 原始样本 | {summary["raw_date_min"]} | {summary["raw_date_max"]} |
| 清洗后样本 | {summary["clean_date_min"]} | {summary["clean_date_max"]} |

## 清洗前后行为类型分布

{markdown_table(dist)}

## 说明

- 原始样本保留淘宝 UserBehavior 数据集的原始字段：`user_id`、`item_id`、`category_id`、`behavior_type`、`timestamp`。
- 时间戳先从 Unix 秒转换到 `{DEFAULT_TIMEZONE}`，再生成 `date`、`hour`、`weekday` 字段。
- 当前提交的样本适合作品集规模分析。如果希望样本代表性更强，可下载完整数据集后使用 `--sample-mode random --random-state 42` 重新抽样。
"""
    (REPORTS_DIR / "data_quality_report.md").write_text(content, encoding="utf-8")


def write_analysis_summary(df: pd.DataFrame, quality: dict[str, object]) -> None:
    metrics = summarize_behavior_metrics(df)
    repurchase = repurchase_analysis(df)
    behavior_dist = behavior_type_distribution(df)
    behavior_dist["behavior_share"] = behavior_dist["behavior_share"].map(pct)
    behavior_dist = behavior_dist.rename(
        columns={
            "behavior_type": "行为类型",
            "behavior_count": "行为次数",
            "behavior_share": "行为占比",
        }
    )
    top_categories = top_categories_by_purchase(df, top_n=10)
    top_categories = top_categories.rename(
        columns={
            "category_id": "品类ID",
            "purchase_count": "购买次数",
            "buyer_count": "购买用户数",
        }
    )
    category_conversion = category_conversion_analysis(df, top_n=10)
    category_conversion["browse_to_buy_rate"] = category_conversion["browse_to_buy_rate"].map(pct)
    category_conversion["cart_to_buy_rate"] = category_conversion["cart_to_buy_rate"].map(pct)
    category_conversion = category_conversion.rename(
        columns={
            "category_id": "品类ID",
            "buy_count": "购买次数",
            "cart_count": "加购次数",
            "fav_count": "收藏次数",
            "pv_count": "浏览次数",
            "browse_to_buy_rate": "浏览-购买转化率",
            "cart_to_buy_rate": "加购-购买转化率",
        }
    )
    strict_funnel = user_item_sequential_funnel(df)
    user_funnel = user_level_funnel(df)
    user_funnel["conversion_from_view"] = user_funnel["conversion_from_view"].map(pct)
    user_funnel["step"] = user_funnel["step"].map(
        {
            "01_viewed": "01_浏览",
            "02_favorited": "02_收藏",
            "03_added_to_cart": "03_加购",
            "04_purchased": "04_购买",
        }
    )
    user_funnel = user_funnel.rename(columns={"step": "漏斗步骤", "users": "用户数", "conversion_from_view": "相对浏览转化率"})
    segmentation = user_segmentation(df)
    segmentation["avg_active_days"] = segmentation["avg_active_days"].round(2)
    segmentation["avg_purchase_count"] = segmentation["avg_purchase_count"].round(2)
    segmentation["avg_cart_count"] = segmentation["avg_cart_count"].round(2)
    segmentation["behavior_depth"] = segmentation["behavior_depth"].map(
        {
            "browse_only": "仅浏览",
            "favorited": "已收藏",
            "added_to_cart": "已加购未购买",
            "purchased": "已购买",
        }
    )
    segmentation["purchase_segment"] = segmentation["purchase_segment"].astype(str).map(
        {
            "no_purchase": "未购买",
            "one_purchase": "购买1次",
            "two_to_three": "购买2-3次",
            "four_plus": "购买4次及以上",
        }
    )
    segmentation = segmentation.rename(
        columns={
            "behavior_depth": "行为深度",
            "purchase_segment": "购买分层",
            "users": "用户数",
            "avg_active_days": "平均活跃天数",
            "total_purchases": "总购买次数",
            "avg_purchase_count": "人均购买次数",
            "avg_cart_count": "人均加购次数",
        }
    )

    hourly_buy = df[df["behavior_type"] == "buy"].groupby("hour").size()
    hourly_total = df.groupby("hour").size()
    daily_purchases = daily_purchase_trend(df)
    dau = daily_active_users(df)

    metric_table = pd.DataFrame(
        [
            ["原始行数", quality["raw_rows"]],
            ["清洗后行数", quality["clean_rows"]],
            ["总行为次数", metrics["total_behaviors"]],
            ["独立用户数（UV）", metrics["uv"]],
            ["商品数", metrics["item_count"]],
            ["品类数", metrics["category_count"]],
            ["浏览次数（PV）", metrics["pv_count"]],
            ["收藏次数", metrics["fav_count"]],
            ["加购次数", metrics["cart_count"]],
            ["购买次数", metrics["buy_count"]],
            ["用户级浏览-购买转化率", pct(metrics["browse_to_purchase_user_rate"])],
            ["用户级加购-购买转化率", pct(metrics["cart_to_purchase_user_rate"])],
            ["用户-商品级顺序浏览-购买转化率", pct(strict_funnel["pv_to_buy_pair_rate"])],
            ["用户-商品级顺序加购-购买转化率", pct(strict_funnel["cart_to_buy_pair_rate"])],
            ["复购率", pct(repurchase["repurchase_rate"])],
            ["加购未购买用户数", len(cart_without_purchase_users(df))],
        ],
        columns=["指标", "数值"],
    )

    strict_funnel_table = pd.DataFrame(
        [
            ["发生过浏览的用户-商品对", strict_funnel["viewed_pairs"]],
            ["发生过加购的用户-商品对", strict_funnel["carted_pairs"]],
            ["发生过购买的用户-商品对", strict_funnel["bought_pairs"]],
            ["先浏览后加购的用户-商品对", strict_funnel["pv_to_cart_pairs"]],
            ["先浏览后购买的用户-商品对", strict_funnel["pv_to_buy_pairs"]],
            ["先加购后购买的用户-商品对", strict_funnel["cart_to_buy_pairs"]],
            ["顺序浏览-加购转化率", pct(strict_funnel["pv_to_cart_pair_rate"])],
            ["顺序浏览-购买转化率", pct(strict_funnel["pv_to_buy_pair_rate"])],
            ["顺序加购-购买转化率", pct(strict_funnel["cart_to_buy_pair_rate"])],
        ],
        columns=["指标", "数值"],
    )

    peak_table = pd.DataFrame(
        [
            ["总活跃高峰小时", f"{int(hourly_total.idxmax()):02d}:00"],
            ["总活跃高峰行为次数", int(hourly_total.max())],
            ["购买高峰小时", f"{int(hourly_buy.idxmax()):02d}:00"],
            ["购买高峰购买次数", int(hourly_buy.max())],
            ["DAU 高峰日期", str(dau.loc[dau["dau"].idxmax(), "date"])],
            ["DAU 高峰用户数", int(dau["dau"].max())],
            ["购买高峰日期", str(daily_purchases.loc[daily_purchases["purchase_count"].idxmax(), "date"])],
            ["单日最高购买次数", int(daily_purchases["purchase_count"].max())],
        ],
        columns=["指标", "数值"],
    )

    content = f"""# 分析汇总

数据集：从公开淘宝 `UserBehavior.csv` 数据集中抽取的 100,000 行真实样本。

时区口径：`{DEFAULT_TIMEZONE}`。

## 核心指标

{markdown_table(metric_table)}

## 行为类型分布

{markdown_table(behavior_dist)}

## 用户级漏斗

该漏斗统计每个用户是否出现过对应行为，适合用于用户层面的总体转化观察，但不限制同一商品，也不限制行为发生顺序。

{markdown_table(user_funnel)}

## 用户-商品级顺序漏斗

该漏斗以 `user_id + item_id` 为分析对象，并要求后续行为发生在前序行为之后，更接近真实商品转化路径。

{markdown_table(strict_funnel_table)}

## 购买次数 Top 品类

{markdown_table(top_categories)}

## 品类转化分析

下表仅保留浏览次数至少为 30 的品类，避免极小样本导致转化率失真。

{markdown_table(category_conversion)}

## 用户分层

{markdown_table(segmentation)}

## 高峰表现

{markdown_table(peak_table)}
"""
    (REPORTS_DIR / "analysis_summary.md").write_text(content, encoding="utf-8")


def write_business_insights(df: pd.DataFrame) -> None:
    metrics = summarize_behavior_metrics(df)
    repurchase = repurchase_analysis(df)
    strict_funnel = user_item_sequential_funnel(df)
    cart_no_buy = cart_without_purchase_users(df)
    top_category = top_categories_by_purchase(df, top_n=1).iloc[0]
    category_conversion = category_conversion_analysis(df, top_n=1).iloc[0]
    hourly_buy = df[df["behavior_type"] == "buy"].groupby("hour").size()
    peak_buy_hour = int(hourly_buy.idxmax())

    content = f"""# 业务洞察

本报告基于公开淘宝 `UserBehavior.csv` 数据集抽取的 100,000 行真实样本。清洗后共保留 {metrics["total_behaviors"]:,} 条有效行为记录，覆盖 {metrics["uv"]:,} 名用户。所有涉及日期和小时的指标均按 `{DEFAULT_TIMEZONE}` 统计。

## 1. 浏览行为占据绝对主体

浏览行为共有 {metrics["pv_count"]:,} 次，购买行为共有 {metrics["buy_count"]:,} 次。整体上看，用户行为主要集中在漏斗顶部，真正进入交易层的行为明显更少。

运营建议：转化优化不应平均面向所有浏览用户，而应优先关注已经表现出明确兴趣的用户，尤其是加购用户和收藏用户。

验证指标：活动或页面优化后，重点观察购买转化率、加购-购买转化率和购买用户数是否提升。

## 2. 用户级转化较高，但严格商品路径转化明显更低

用户级浏览-购买转化率为 {pct(metrics["browse_to_purchase_user_rate"])}，但用户-商品级顺序浏览-购买转化率只有 {pct(strict_funnel["pv_to_buy_pair_rate"])}。

业务解释：很多用户在样本窗口内既浏览又购买，但绝大多数被浏览过的具体商品并没有被购买。用户级指标适合看整体人群转化，用户-商品级顺序指标更适合评估真实商品路径。

运营建议：对外汇报用户整体表现时可以使用用户级转化率；做商品推荐、详情页优化或品类运营时，应优先使用更严格的用户-商品级顺序转化率。

## 3. 加购用户是高意向转化人群

用户级加购-购买转化率为 {pct(metrics["cart_to_purchase_user_rate"])}，用户-商品级顺序加购-购买转化率为 {pct(strict_funnel["cart_to_buy_pair_rate"])}。

运营建议：对加购未购买用户优先尝试购物车提醒、优惠券、降价提醒和限时促销触达。

验证指标：对比触达后的购买率、新增购买用户数和复购率，判断触达策略是否有效。

## 4. 小时行为必须按本地业务时间解释

将时间戳转换为 `{DEFAULT_TIMEZONE}` 后，购买高峰小时为 {peak_buy_hour:02d}:00。

运营建议：安排活动推送、首页资源位和日常运营节奏时，应使用本地小时口径，避免直接使用 UTC 小时导致误判。

## 5. 品类表现需要同时看规模和转化效率

当前样本中，品类 `{int(top_category["category_id"])}` 的购买次数最高，共 {int(top_category["purchase_count"])} 次。在满足基础浏览量的品类中，品类 `{int(category_conversion["category_id"])}` 也在品类转化表中表现突出。

运营建议：区分“高购买规模品类”和“高转化效率品类”。前者适合承接流量和资源位，后者适合做推荐位测试、精准促销或长尾品类机会挖掘。

## 6. 复购用户是留存运营的重要人群

在 {repurchase["total_buyers"]:,} 名购买用户中，有 {repurchase["repurchase_users"]:,} 名用户至少购买 2 次，复购率为 {pct(repurchase["repurchase_rate"])}。

运营建议：将复购用户与一次性购买用户分开分析，围绕高频购买用户设计会员、权益、个性化推荐和留存策略。

## 7. 加购未购买用户适合作为再营销人群

样本中共有 {len(cart_no_buy):,} 名用户发生过加购行为但没有购买。

运营建议：将该人群作为再营销候选用户，在真实业务中可用于优惠券提醒、库存提醒、降价提醒和限时活动触达。

## 8. 高价值用户贡献了更集中的购买行为

当前样本中购买次数最高的用户购买了 {int(high_value_users(df, top_n=1).iloc[0]["purchase_count"])} 次，说明购买行为在少量高价值用户中更集中。

运营建议：结合购买频次、活跃天数和购买商品丰富度构建用户价值评分，用于留存优先级排序和会员运营分层。
"""
    (REPORTS_DIR / "business_insights.md").write_text(content, encoding="utf-8")


def records(df: pd.DataFrame) -> list[dict[str, object]]:
    safe_df = df.copy()
    for column in safe_df.columns:
        if pd.api.types.is_datetime64_any_dtype(safe_df[column]):
            safe_df[column] = safe_df[column].astype(str)
    return safe_df.to_dict(orient="records")


def write_dashboard_data(df: pd.DataFrame, quality: dict[str, object]) -> None:
    metrics = summarize_behavior_metrics(df)
    repurchase = repurchase_analysis(df)
    strict_funnel = user_item_sequential_funnel(df)

    daily = daily_active_users(df).merge(daily_purchase_trend(df), on="date", how="left").fillna(0)
    daily["date"] = daily["date"].astype(str)
    hourly = (
        hourly_activity(df)
        .pivot_table(index="hour", columns="behavior_type", values="behavior_count", fill_value=0)
        .reset_index()
        .rename_axis(None, axis=1)
    )
    for column in ["pv", "fav", "cart", "buy"]:
        if column not in hourly.columns:
            hourly[column] = 0
    hourly = hourly[["hour", "pv", "fav", "cart", "buy"]]

    payload = {
        "meta": {
            "timezone": DEFAULT_TIMEZONE,
            "raw_rows": quality["raw_rows"],
            "clean_rows": quality["clean_rows"],
            "date_min": quality["clean_date_min"],
            "date_max": quality["clean_date_max"],
        },
        "kpis": [
            {"metric": "总行为次数", "value": metrics["total_behaviors"]},
            {"metric": "独立用户数（UV）", "value": metrics["uv"]},
            {"metric": "购买次数", "value": metrics["buy_count"]},
            {"metric": "用户级浏览-购买转化率", "value": metrics["browse_to_purchase_user_rate"]},
            {"metric": "顺序浏览-购买转化率", "value": strict_funnel["pv_to_buy_pair_rate"]},
            {"metric": "顺序加购-购买转化率", "value": strict_funnel["cart_to_buy_pair_rate"]},
            {"metric": "复购率", "value": repurchase["repurchase_rate"]},
            {"metric": "加购未购买用户数", "value": len(cart_without_purchase_users(df))},
        ],
        "behavior_distribution": records(behavior_type_distribution(df)),
        "daily_trends": records(daily),
        "hourly_activity": records(hourly),
        "top_categories": records(top_categories_by_purchase(df, top_n=10)),
        "category_conversion": records(category_conversion_analysis(df, top_n=10)),
        "user_funnel": records(user_level_funnel(df)),
        "user_segmentation": records(user_segmentation(df)),
    }
    DASHBOARD_DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data(CLEANED_PATH)
    raw_df = pd.read_csv(RAW_PATH)
    quality = data_quality_summary(RAW_PATH, df)
    save_figures(df)
    write_data_quality_report(quality, raw_df, df)
    write_analysis_summary(df, quality)
    write_business_insights(df)
    write_dashboard_data(df, quality)
    print(f"Generated reports under {REPORTS_DIR}")
    print(f"Generated figures under {FIGURES_DIR}")


if __name__ == "__main__":
    main()
