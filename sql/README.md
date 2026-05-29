# SQL 使用说明

本目录中的 PostgreSQL 查询基于清洗后的 CSV 文件：`data/cleaned_user_behavior.csv`。

## 建表语句

```sql
DROP TABLE IF EXISTS user_behavior;

CREATE TABLE user_behavior (
    user_id BIGINT,
    item_id BIGINT,
    category_id BIGINT,
    behavior_type VARCHAR(10),
    behavior_name_en VARCHAR(50),
    behavior_name_cn VARCHAR(20),
    timestamp BIGINT,
    behavior_time TIMESTAMP,
    date DATE,
    hour INT,
    weekday VARCHAR(20)
);
```

## 导入 CSV

在 PostgreSQL 中使用本机绝对路径导入：

```sql
COPY user_behavior
FROM 'C:/Users/blues/Desktop/电商分析/Taobao-User-Behavior-Conversion-Analysis/data/cleaned_user_behavior.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');
```

如果 PostgreSQL 服务端没有权限读取本机路径，可以在项目根目录使用 `psql` 的 `\copy`：

```bash
\copy user_behavior FROM 'data/cleaned_user_behavior.csv' WITH (FORMAT csv, HEADER true, ENCODING 'UTF8')
```

## 查询覆盖范围

- 整体行为规模
- 行为类型分布
- DAU 和购买趋势
- 小时行为分布
- Top 购买品类
- 用户级转化率
- 用户-商品级顺序漏斗
- 品类级转化分析
- 复购率
- 加购未购买用户
- 高价值用户
- 使用窗口函数计算每日 Top 品类
