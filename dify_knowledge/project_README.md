# Taobao User Behavior & Conversion Funnel Analysis

淘宝用户行为与转化漏斗分析项目

## 项目亮点

- **真实公开样本**：基于淘宝 UserBehavior 公开数据集抽取 100,000 行真实用户行为记录，清洗后保留 99,956 条有效记录，适合作为 GitHub 可复现的数据分析作品集样本。
- **完整分析链路**：覆盖 Python / Pandas 数据清洗、数据质量检查、PostgreSQL SQL 分析、Markdown 报告生成和 Excel 看板展示，呈现从原始数据到业务结论的完整流程。
- **双口径转化漏斗**：同时构建用户级转化漏斗，以及更严格的用户-商品级顺序转化漏斗，区分“用户是否购买过”和“同一商品路径是否完成转化”。
- **运营分析场景明确**：围绕加购未购买用户、复购用户、高价值用户、Top 购买品类和小时行为高峰，输出可用于再营销、留存运营和品类运营的分析建议。
- **能力展示清晰**：项目可体现 Python 数据处理、SQL 指标分析、转化口径拆解、业务洞察表达和 Excel 可视化看板能力，适合数据分析、数据运营、产品运营和 AI 产品测试实习岗位展示。

## 项目概览

本项目基于公开淘宝 `UserBehavior.csv` 数据集抽取的真实样本，构建电商用户行为与转化漏斗分析流程。项目覆盖数据清洗、数据质量检查、SQL 分析、用户转化漏斗、品类转化、复购行为、用户分层和 Excel 看板展示，适合作为数据分析、数据运营、产品运营和 AI 产品测试实习岗位的简历项目。

当前提交的数据文件来自下载后的 `archive.zip` / `UserBehavior.csv`，抽取 100,000 行真实行为记录。按 `Asia/Shanghai` 业务时区清洗后，共保留 99,956 条有效行为记录用于分析。

数据集来源：[Alibaba Tianchi Taobao UserBehavior Dataset](https://tianchi.aliyun.com/dataset/649?lang=en-us)。

## 看板预览

项目已包含 Excel 看板文件：`dashboard/taobao_behavior_dashboard.xlsx`。

![Excel 看板预览](dashboard/dashboard_preview.png)

## 分析问题

- 整体用户行为规模如何，包括总行为次数、UV、商品数和品类数？
- 浏览、收藏、加购、购买四类行为如何分布？
- 用户级浏览-购买转化率是多少？
- 更严格的用户-商品级顺序转化率是多少？
- DAU 和购买次数随日期如何变化？
- 按北京时间统计，哪些小时用户活跃度和购买行为更高？
- 哪些商品品类贡献了最多购买次数？
- 哪些品类既有一定流量规模，又有较强转化效率？
- 是否存在复购用户，高价值用户是否集中？
- 有多少用户加购后没有购买，是否适合作为再营销人群？

## 数据集说明

数据来源为阿里天池公开淘宝用户行为数据集 `UserBehavior.csv`。原始文件没有表头，共 5 个字段：

| 字段 | 说明 |
| --- | --- |
| `user_id` | 脱敏后的用户 ID |
| `item_id` | 脱敏后的商品 ID |
| `category_id` | 脱敏后的商品品类 ID |
| `behavior_type` | 用户行为类型：`pv`、`fav`、`cart`、`buy` |
| `timestamp` | Unix 时间戳 |

行为类型映射：

| behavior_type | English | 中文 |
| --- | --- | --- |
| `pv` | page view | 浏览 |
| `fav` | favorite | 收藏 |
| `cart` | add to cart | 加购 |
| `buy` | purchase | 购买 |

## 技术栈

- Python
- Pandas
- Matplotlib / Seaborn
- PostgreSQL SQL
- Jupyter Notebook
- Excel dashboard
- Dify Knowledge / RAG Demo

## 项目结构

```text
Taobao-User-Behavior-Conversion-Analysis/
|-- README.md
|-- requirements.txt
|-- data/
|   |-- README.md
|   |-- raw_user_behavior_sample.csv
|   `-- cleaned_user_behavior.csv
|-- notebooks/
|   `-- 01_data_cleaning_eda.ipynb
|-- sql/
|   |-- README.md
|   `-- taobao_behavior_analysis.sql
|-- reports/
|   |-- analysis_summary.md
|   |-- business_insights.md
|   |-- data_quality_report.md
|   |-- resume_project_review.md
|   |-- dashboard_data.json
|   `-- figures/
|       |-- behavior_distribution.png
|       |-- daily_trends.png
|       |-- hourly_behavior_heatmap.png
|       `-- top_categories_purchase.png
|-- dashboard/
|   |-- dashboard_design.md
|   |-- dashboard_preview.png
|   `-- taobao_behavior_dashboard.xlsx
|-- dify/
|   |-- README.md
|   |-- knowledge_base_files.md
|   |-- system_prompt.md
|   |-- sample_questions.md
|   `-- app_config_guide.md
|-- dify_knowledge/
|   |-- README.md
|   |-- upload_checklist.md
|   |-- sample_questions.md
|   |-- system_prompt.md
|   `-- app_config_guide.md
|-- screenshots/
|   `-- README.md
`-- src/
    |-- data_cleaning.py
    |-- analysis.py
    |-- generate_reports.py
    |-- prepare_real_data_sample.py
    `-- generate_sample_data.py
```

## 数据清洗流程

清洗脚本同时支持官方无表头 `UserBehavior.csv` 和本项目中已抽取的带表头样本 CSV。

清洗逻辑：

1. 读取原始行为 CSV。
2. 删除重复记录。
3. 删除必要字段缺失的记录。
4. 将 ID 字段和时间戳转换为数值类型。
5. 统一并校验行为类型。
6. 将 Unix 时间戳转换为 `Asia/Shanghai` 本地业务时间。
7. 过滤分析窗口外的异常日期。
8. 构建 `date`、`hour`、`weekday` 字段。
9. 映射中英文行为名称。
10. 导出 `data/cleaned_user_behavior.csv`。

## 核心指标

当前真实样本结果：

| 指标 | 数值 |
| --- | ---: |
| 原始行数 | 100,000 |
| 清洗后行数 | 99,956 |
| 独立用户数（UV） | 983 |
| 商品数 | 64,440 |
| 品类数 | 3,128 |
| 浏览次数（PV） | 89,665 |
| 收藏次数 | 2,744 |
| 加购次数 | 5,446 |
| 购买次数 | 2,101 |
| 用户级浏览-购买转化率 | 68.27% |
| 用户级加购-购买转化率 | 72.89% |
| 用户-商品级顺序浏览-购买转化率 | 1.46% |
| 用户-商品级顺序加购-购买转化率 | 6.02% |
| 复购率 | 65.87% |
| 加购未购买用户数 | 196 |

## 指标口径说明

- **用户级浏览-购买转化率较高的原因**：本项目样本来自已经发生过行为的用户记录，不包含完整曝光人群、站外访客或未产生行为的真实访客，因此不能等同于淘宝平台真实访客转化率。
- **用户级转化率的含义**：用户级浏览-购买转化率衡量的是“一个用户在样本窗口内是否既发生过浏览，也发生过购买”，适合观察样本用户整体是否进入过购买阶段。
- **用户-商品级顺序转化率的含义**：用户-商品级顺序转化率以 `user_id + item_id` 为分析对象，并要求同一用户对同一商品按时间顺序从浏览或加购走向购买，口径更严格，更接近具体商品路径转化。
- **为什么两个指标要同时展示**：用户级指标有助于理解人群整体购买覆盖，用户-商品级顺序指标有助于评估具体商品路径效率。两个转化率一起展示，可以避免只看单一高转化率而误判业务表现。

分析覆盖：

- 总行为次数、UV、商品数、品类数
- 行为类型分布和行为占比
- 清洗前后数据质量检查
- 用户级转化漏斗
- 带时间顺序约束的用户-商品级转化漏斗
- DAU 和每日购买趋势
- `Asia/Shanghai` 口径下的小时行为分布
- 购买次数 Top 品类
- 品类级浏览-购买、加购-购买转化率
- 复购率
- 加购未购买用户
- 高价值用户
- 按行为深度和购买频次划分的用户分层

## SQL 分析

`sql/taobao_behavior_analysis.sql` 包含以下 PostgreSQL 查询：

- 整体行为规模
- 行为类型分布和占比
- DAU
- 每日购买次数和购买用户数
- 小时行为分布
- Top 10 购买品类
- 浏览-购买转化率
- 加购-购买转化率
- 收藏-购买转化率
- 复购率
- 加购未购买用户
- 高价值用户
- 基于 CTE 的用户漏斗
- 使用窗口函数计算每日购买 Top 品类
- 带时间顺序约束的用户-商品级漏斗
- 品类级转化分析

## 看板和报告

看板产物：

- `dashboard/taobao_behavior_dashboard.xlsx`：Excel 看板文件。
- `dashboard/dashboard_preview.png`：看板预览图。
- `dashboard/dashboard_design.md`：看板设计说明。

生成报告：

- `reports/data_quality_report.md`：数据质量检查和清洗影响。
- `reports/analysis_summary.md`：核心指标、严格漏斗、品类转化和用户分层。
- `reports/business_insights.md`：面向业务动作的分析洞察和验证指标。
- `reports/figures/`：可用于 README、报告或展示材料的图表图片。
  - `reports/figures/behavior_distribution.png`：行为类型分布。
  - `reports/figures/daily_trends.png`：DAU 与购买趋势。
  - `reports/figures/hourly_behavior_heatmap.png`：小时行为热力图。
  - `reports/figures/top_categories_purchase.png`：购买次数 Top 品类。

## Dify AI 问答助手扩展

本项目基于 Dify Knowledge 构建了一个项目问答助手 Demo，将 README、分析总结、业务洞察、数据质量报告、SQL 说明和看板说明接入知识库，用于展示“数据分析 + AI 应用产品化”的能力。该 Demo 基于公开数据集样本和项目文档构建，适合作为个人作品集展示，不代表企业级生产系统，也没有训练或微调大模型。

Dify Web App：[https://udify.app/chat/0nIFW08DLfoL8IzA](https://udify.app/chat/0nIFW08DLfoL8IzA)

助手可回答的问题包括：

- 项目背景、数据来源和样本口径。
- 数据清洗流程、异常时间过滤和北京时间转换。
- 核心指标口径，尤其是用户级转化率与用户-商品级顺序转化率的区别。
- SQL 分析覆盖范围、CTE 和窗口函数使用场景。
- 业务洞察、运营动作和验证指标。
- Excel 看板设计思路和展示重点。
- 面试表达、一分钟项目介绍和简历 bullet。

实现原理：这是一个 RAG 问答助手，不是微调模型，也不是训练大模型，更不是实时读取 CSV 重新分析。配置流程是先上传项目文档，Dify 对文档分块，并使用 embedding 模型建立语义索引；用户提问时先检索相关文档片段，再由大模型结合检索结果和系统提示词生成回答。开启 Citation / Attribution 后，可以展示回答来源。

当前仓库尚未包含 Dify Demo 截图，可补充 Dify Demo 截图。

## 业务洞察

当前结论基于 100,000 行公开样本和 99,956 条清洗后有效行为记录，适合作为样本分析结果解读，不代表平台全量真实经营水平。

### 1. 浏览行为占据漏斗顶部，转化优化应优先聚焦高意向人群

- **发现**：PV 为 89,665 次，占有效行为的 89.70%；购买行为为 2,101 次，占 2.10%。
- **解释**：样本中的用户行为主要集中在浏览阶段，直接面向所有浏览用户做转化动作效率可能较低。
- **可执行动作**：优先筛选加购、收藏、重复浏览和高活跃用户，针对不同意向层级设计商品提醒、优惠券、活动入口或个性化推荐。
- **可验证指标**：观察加购-购买转化率、购买用户数、购买次数；若后续接入金额字段，可进一步验证 GMV 变化。

### 2. 用户级转化率与用户-商品级顺序转化率差异明显，需要分场景解读

- **发现**：用户级浏览-购买转化率为 68.27%，但用户-商品级顺序浏览-购买转化率仅为 1.46%。
- **解释**：很多用户在样本窗口内既浏览又购买，但购买的未必是曾经浏览过的同一件商品；因此用户级指标适合看人群购买覆盖，用户-商品级指标更适合看具体商品路径转化。
- **可执行动作**：对外展示整体人群表现时使用用户级漏斗；评估详情页、推荐策略或商品运营时，优先使用用户-商品级顺序漏斗。
- **可验证指标**：同时跟踪用户级浏览-购买转化率、用户-商品级顺序浏览-购买转化率和用户-商品级顺序加购-购买转化率。

### 3. 加购未购买用户适合作为再营销候选人群

- **发现**：样本中有 196 名用户发生过加购但未购买；用户级加购-购买转化率为 72.89%，说明加购用户整体购买意向更强。
- **解释**：加购行为通常代表用户已经进入决策阶段，但可能受到价格、库存、对比商品或购买时机影响而暂未下单。
- **可执行动作**：对加购未购买用户进行购物车提醒、优惠券触达、降价提醒、库存提醒或相似商品推荐，并区分高频加购用户与低频加购用户。
- **可验证指标**：对比触达组与未触达组的购买率、加购-购买转化率、购买次数、复购率；如有金额字段，可验证 GMV 和客单价变化。

### 4. 复购用户值得单独做留存和会员运营

- **发现**：购买用户中复购用户占比为 65.87%，说明样本内存在较明显的重复购买行为。
- **解释**：复购用户通常比一次性购买用户更适合作为留存运营对象，也更适合承接会员权益、定向推荐和品类扩展策略。
- **可执行动作**：将购买用户按购买频次、活跃天数和购买品类丰富度分层，对高复购用户设计会员权益、周期性召回和关联品类推荐。
- **可验证指标**：复购率、人均购买次数、活跃天数、购买品类数和高价值用户留存率。

### 5. 时间和品类分析可用于运营资源排期

- **发现**：按 `Asia/Shanghai` 口径统计，购买高峰小时为 13:00；当前样本中 DAU 和购买次数均在 2017-12-03 达到高峰，品类 `2735466` 的购买次数排名第一。
- **解释**：小时高峰可以辅助活动触达和资源位排期，品类购买排名可以辅助识别更适合承接流量的品类。
- **可执行动作**：在购买高峰前后测试消息触达、优惠入口和首页资源位；对高购买规模品类做稳定供给和资源承接，对高转化效率品类做推荐位或促销测试。
- **可验证指标**：分小时购买次数、购买用户数、品类浏览-购买转化率、品类加购-购买转化率和 Top 品类购买占比。

## How to Run

Run the following commands from the project root directory.

Create and activate a virtual environment on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On macOS or Linux, use:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The repository already includes a 100,000-row real sample. To regenerate a small synthetic sample only for testing:

```bash
python src/generate_sample_data.py --rows 5000
```

To rebuild the real public dataset sample, download `UserBehavior.csv` from Tianchi or the Kaggle mirror, put it under `data/UserBehavior.csv`, and extract a GitHub-friendly real sample:

```bash
python src/prepare_real_data_sample.py --input data/UserBehavior.csv --output data/raw_user_behavior_sample.csv --rows 100000
```

For a less biased sample, use fixed-seed random sampling:

```bash
python src/prepare_real_data_sample.py --input data/UserBehavior.csv --output data/raw_user_behavior_sample.csv --rows 100000 --sample-mode random --random-state 42
```

If the downloaded file is `UserBehavior.csv.zip`, you can use it directly without extracting the full CSV:

```bash
python src/prepare_real_data_sample.py --input data/UserBehavior.csv.zip --output data/raw_user_behavior_sample.csv --rows 100000 --sample-mode random --random-state 42
```

Clean the selected raw sample:

```bash
python src/data_cleaning.py --input data/raw_user_behavior_sample.csv --output data/cleaned_user_behavior.csv
```

Run Pandas analysis:

```bash
python src/analysis.py --input data/cleaned_user_behavior.csv
```

Regenerate markdown reports and chart images:

```bash
python src/generate_reports.py
```

Run tests:

```bash
python -m pytest
```

Analyze the full Tianchi dataset directly if your machine has enough memory and storage:

```bash
python src/data_cleaning.py --input data/UserBehavior.csv --output data/cleaned_user_behavior.csv
python src/analysis.py --input data/cleaned_user_behavior.csv
python src/generate_reports.py
```

## Future Improvements

- Add a native Power BI `.pbix` version of the dashboard.
- Add cohort analysis by first purchase date.
- Add RFM-style user segmentation based on frequency and recency.
- Add automated table exports for SQL query results.
- Expand pytest coverage for edge cases and empty datasets.

## Resume Bullet Points 中文简历写法参考

淘宝用户行为与转化漏斗分析项目｜个人项目｜Python / Pandas / PostgreSQL / SQL / Excel

正式简历精简版：

- 基于淘宝 UserBehavior 公开数据集抽取 10 万行真实行为样本，完成数据清洗、异常时间过滤、北京时间转换与分析字段构建，保留 99,956 条有效记录用于分析。
- 使用 Pandas 与 PostgreSQL 统计 PV、UV、购买次数、复购率、用户级转化率和用户-商品级顺序转化率，区分整体人群转化与具体商品路径转化。
- 通过 CTE、CASE WHEN、GROUP BY 和窗口函数分析 DAU、小时活跃、Top 购买品类、高价值用户和 196 名加购未购买用户，输出再营销与留存运营建议。
- 构建 Excel 看板展示核心 KPI、行为分布、购买趋势、品类排名和用户分层，并沉淀可复现的数据处理、报告生成和可视化展示流程。

展开版写法参考：

- 基于淘宝 UserBehavior 公开数据集，构建电商用户行为与转化漏斗分析项目，分析浏览、收藏、加购、购买等行为路径。
- 使用 Pandas 完成数据清洗、北京时间转换、异常时间过滤和行为标签构建，沉淀可复现的数据处理与报告生成脚本。
- 通过 SQL 和 Pandas 统计用户规模、行为分布、用户级转化率、用户-商品级顺序转化率、复购率和加购未购买用户。
- 使用 CTE、CASE WHEN、GROUP BY 和窗口函数分析 DAU、购买趋势、品类购买排名、复购用户和高价值用户。
- 构建 Excel 看板展示核心 KPI、行为分布、DAU 趋势、购买趋势、Top 品类和用户分层，并输出面向运营动作的业务洞察。

AI 扩展功能可选写法：

- 基于 Dify Knowledge 构建电商数据分析项目 AI 问答助手，将 README、分析报告、业务洞察和数据质量报告接入知识库，支持项目背景、指标口径、运营建议和面试表达的自然语言问答。
- 使用 Dify 搭建 RAG 问答 Demo，对项目文档进行分块、向量化和知识库检索，并通过系统提示词约束回答边界，支持带引用的项目问答与指标解释。
