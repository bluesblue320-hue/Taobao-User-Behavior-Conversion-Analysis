from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from data_cleaning import clean_user_behavior


def test_clean_user_behavior_converts_timestamp_to_shanghai_time(tmp_path):
    raw_path = tmp_path / "raw.csv"
    output_path = tmp_path / "cleaned.csv"
    raw_path.write_text(
        "user_id,item_id,category_id,behavior_type,timestamp\n"
        "1,10,100,pv,1511568000\n",
        encoding="utf-8",
    )

    df = clean_user_behavior(raw_path, output_path)

    assert len(df) == 1
    assert str(df.loc[0, "behavior_time"]) == "2017-11-25 08:00:00"
    assert df.loc[0, "date"] == "2017-11-25"
    assert df.loc[0, "hour"] == 8
    assert df.loc[0, "behavior_name_cn"] == "浏览"
