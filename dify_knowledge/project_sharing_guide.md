# 项目发送与打包说明

本文档用于说明：如果要把本项目发给 HR、面试官、技术同学或上传 GitHub，应该发送哪些内容，以及哪些文件不应该发送。

## 一、推荐发送方式

最推荐的方式是：

1. 上传到 GitHub。
2. 在简历中放 GitHub 项目链接。
3. 如果对方要求附件，再发送项目压缩包。

这样比直接发一堆文件更专业，也方便对方快速浏览 README、代码、报告和看板。

## 二、发给面试官或技术同学

如果对方会看代码、SQL 和项目结构，建议发送完整项目目录：

```text
Taobao-User-Behavior-Conversion-Analysis/
```

建议包含：

```text
README.md
requirements.txt
src/
sql/
data/
reports/
dashboard/
tests/
notebooks/
```

### 重点文件说明

| 路径 | 作用 |
| --- | --- |
| `README.md` | 项目首页说明，包含项目背景、指标、看板预览和运行方法 |
| `requirements.txt` | Python 依赖，方便复现环境 |
| `src/data_cleaning.py` | 数据清洗脚本 |
| `src/analysis.py` | 核心分析函数 |
| `src/generate_reports.py` | 自动生成分析报告和图表 |
| `sql/taobao_behavior_analysis.sql` | PostgreSQL 分析 SQL |
| `sql/README.md` | SQL 建表和导入说明 |
| `data/raw_user_behavior_sample.csv` | 100,000 行真实样本数据 |
| `data/cleaned_user_behavior.csv` | 清洗后的分析数据 |
| `reports/analysis_summary.md` | 中文分析汇总 |
| `reports/business_insights.md` | 中文业务洞察 |
| `reports/data_quality_report.md` | 中文数据质量报告 |
| `reports/figures/` | 分析图表 |
| `dashboard/taobao_behavior_dashboard.xlsx` | Excel 看板文件 |
| `dashboard/dashboard_preview.png` | 看板预览图 |
| `tests/` | 基础测试，展示工程化和口径校验意识 |
| `notebooks/01_data_cleaning_eda.ipynb` | Notebook 版清洗和 EDA 流程 |

## 三、发给 HR 或非技术人员

如果对方主要看结果，不一定看代码，可以发送精简材料。

建议包含：

```text
README.md
reports/business_insights.md
reports/analysis_summary.md
reports/data_quality_report.md
dashboard/taobao_behavior_dashboard.xlsx
dashboard/dashboard_preview.png
```

也可以附一句说明：

> 完整项目包含 Python 数据清洗、SQL 分析、数据质量报告、转化漏斗、用户分层和 Excel 看板，可提供 GitHub 链接或完整压缩包。

## 四、上传 GitHub 时应包含的内容

建议上传：

```text
README.md
PROJECT_SHARING_GUIDE.md
requirements.txt
.gitignore
src/
sql/
data/README.md
data/raw_user_behavior_sample.csv
data/cleaned_user_behavior.csv
reports/
dashboard/
tests/
notebooks/
screenshots/
dify_knowledge/
```

上传前确认：

- README 中的看板图片能正常显示。
- `reports/analysis_summary.md`、`reports/business_insights.md`、`reports/data_quality_report.md` 都是中文。
- `dashboard/taobao_behavior_dashboard.xlsx` 可以打开。
- `python -m pytest` 能通过。
- 不要把完整原始大文件传上去。

## 五、不应该发送或上传的内容

以下内容不要放进压缩包，也不要上传 GitHub：

```text
.venv/
__pycache__/
.ipynb_checkpoints/
node_modules/
data/UserBehavior.csv
data/UserBehavior.csv.zip
data/*.zip
*.pyc
.DS_Store
```

原因：

- `.venv/`、`node_modules/` 体积大，且可通过依赖重新安装。
- `__pycache__/`、`*.pyc` 是运行缓存文件，没有展示价值。
- `data/UserBehavior.csv` 和 zip 原始数据体积太大，不适合上传。
- 项目已经包含 `raw_user_behavior_sample.csv` 和 `cleaned_user_behavior.csv`，足够展示和复现。

## 六、建议压缩包名称

如果需要发压缩包，建议命名为：

```text
Taobao-User-Behavior-Analysis-Portfolio.zip
```

或者中文：

```text
淘宝用户行为分析项目_作品集.zip
```

## 七、邮件或消息发送模板

可以这样发给面试官或 HR：

```text
您好，这是我的电商用户行为分析项目作品。

项目基于淘宝 UserBehavior 公开数据集，完成了 Python 数据清洗、SQL 分析、数据质量检查、用户转化漏斗、品类转化、用户分层和 Excel 看板展示。

核心结果包括：
- 清洗后共 99,956 条有效行为记录；
- 统计 PV、UV、购买次数、复购率、用户级转化率和用户-商品级顺序转化率；
- 识别加购未购买用户、高购买品类和高价值用户；
- 输出中文分析报告和 Excel 看板。

项目入口请查看 README.md。
```

## 八、最终建议

如果是正式投递，优先使用 GitHub 链接；如果对方要求附件，再发送完整压缩包。

如果只是先给 HR 快速看，可以发送 README、业务洞察报告和 Excel 看板。

如果是发给技术面试官，建议发送完整项目，因为代码、SQL、测试和报告都能体现项目完整度。

## 九、Dify Demo 展示建议

面试时可以展示 Dify Web App，用于说明本项目除了传统数据分析链路外，还尝试把项目文档整理成可问答的 RAG Demo。

推荐演示问题：

- 为什么用户级转化率比用户-商品级顺序转化率高？
- 加购未购买用户有什么运营价值？
- 请用一分钟介绍这个项目。

展示重点是：Dify 基于项目 README、分析报告、业务洞察、数据质量报告、SQL 说明和看板说明进行知识库检索，帮助回答指标解释、业务洞察、项目讲解和简历表达问题。演示时应强调这是个人作品集中的 RAG 问答 Demo，不是实时 BI 系统，也不是企业级生产系统，不要表述为实时读取 CSV 重新分析。
