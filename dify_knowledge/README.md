# Dify Knowledge 文档资料包

这个目录用于整理“淘宝用户行为分析项目 AI 问答助手”上传到 Dify Knowledge 前需要准备的项目资料。内容来自当前项目已有 README、分析报告、业务洞察、数据质量报告、SQL 说明、看板说明和项目分享说明，用于支持助手回答项目背景、数据来源、清洗流程、指标口径、SQL 分析、业务洞察、看板设计和面试表达等问题。

该功能定位为个人作品集 Demo，用于展示“数据分析 + AI 应用产品化”的能力。它基于公开数据集样本和项目文档构建，不是企业级生产系统，也不代表淘宝平台全量经营结论。

## 建议上传到 Dify Knowledge 的文件

| 文件 | 来源 | 作用 | 状态 |
| --- | --- | --- | --- |
| `project_README.md` | `README.md` | 项目总览、数据来源、技术栈、核心指标、运行方式和简历表达入口 | 已整理 |
| `analysis_summary.md` | `reports/analysis_summary.md` | 核心指标、行为分布、用户级漏斗、用户-商品级顺序漏斗、品类转化、用户分层和高峰表现 | 已整理 |
| `business_insights.md` | `reports/business_insights.md` | 面向运营动作的业务洞察、解释、建议和验证指标 | 已整理 |
| `data_quality_report.md` | `reports/data_quality_report.md` | 数据清洗影响、异常时间过滤、清洗前后行数和字段说明 | 已整理 |
| `dashboard_design.md` | `dashboard/dashboard_design.md` | Excel 看板页面结构、KPI、图表设计和展示原则 | 已整理 |
| `sql_README.md` | `sql/README.md` | PostgreSQL 建表、CSV 导入方式和 SQL 查询覆盖范围 | 已整理 |
| `project_sharing_guide.md` | `PROJECT_SHARING_GUIDE.md` | 项目投递、打包、发送给 HR 或技术面试官时的材料说明 | 已整理 |

本次检查中，上述优先文件均存在；没有发现需要在此标注“该文件当前不存在，需要后续补充”的指定文件。

如果直接从项目原始目录上传，也可以优先选择：

- `README.md`
- `reports/analysis_summary.md`
- `reports/business_insights.md`
- `reports/data_quality_report.md`
- `dashboard/dashboard_design.md`
- `sql/README.md`
- `PROJECT_SHARING_GUIDE.md`

## 辅助文件

| 文件 | 作用 |
| --- | --- |
| `upload_checklist.md` | 上传 Dify 前的文件清单、检查项、分块建议和检索测试问题 |
| `sample_questions.md` | 用于测试问答助手效果的 28 个样例问题 |
| `system_prompt.md` | 可复制到 Dify Chatbot / Chatflow 的系统提示词 |
| `app_config_guide.md` | Dify Knowledge、Chatbot、引用归属和 Web App 发布配置说明 |

辅助文件主要用于配置和测试，不一定要上传到 Knowledge。建议先把系统提示词放入 Dify 的系统提示词区域，把 `sample_questions.md` 作为人工测试材料使用。

## 不建议上传的文件

不要上传以下文件或目录到 Dify Knowledge：

- `data/UserBehavior.csv`
- `data/UserBehavior.csv.zip`
- `data/*.zip`
- `.venv/`
- `__pycache__/`
- `node_modules/`
- `*.pyc`
- `dashboard/*.xlsx`

也不建议把完整大数据文件、缓存目录、虚拟环境、运行产物或无关二进制依赖上传到知识库。`dashboard/taobao_behavior_dashboard.xlsx` 和 `dashboard/dashboard_preview.png` 可作为作品集展示附件保留，但 Dify Knowledge 首轮建议优先上传 Markdown 文档，避免图片或 Excel 文件解析不稳定。

## 实现原理

这是一个 RAG 问答助手，不是微调模型，也不是训练大模型，更不是实时读取 CSV 重新分析。使用时先上传项目文档，Dify 会对文档分块，并通过 embedding 模型建立语义索引；用户提问时，系统先检索相关文档片段，再让大模型基于检索结果和系统提示词生成回答。开启 Citation / Attribution 后，可以显示回答依据来自哪些文档。

## 上传后可以回答的问题

上传上述 Markdown 文档后，Dify 助手可以基于知识库回答：

- 项目为什么选择淘宝 UserBehavior 公开数据集，以及样本规模是多少。
- 数据清洗做了哪些步骤，为什么清洗后保留 99,956 条有效记录。
- PV、UV、购买次数、复购率、用户级转化率、用户-商品级顺序转化率等指标如何定义。
- 为什么用户级浏览-购买转化率和用户-商品级顺序浏览-购买转化率差异很大。
- 哪些业务洞察可以支持再营销、留存运营、品类运营和活动排期。
- SQL 分析覆盖哪些查询场景，如何在 PostgreSQL 中建表和导入 CSV。
- Excel 看板包含哪些页面、KPI 和图表。
- 这个项目如何写进简历，如何向 HR 或面试官解释。

回答时应始终提醒：本项目基于公开数据集抽样和个人作品集分析，不应表述为企业内部真实生产系统或平台全量经营结论。
