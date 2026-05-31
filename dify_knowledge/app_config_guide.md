# Dify App 配置说明

本说明用于在 Dify 网页端配置“淘宝用户行为分析项目 AI 问答助手”。这里只描述个人作品集 Demo 的配置流程，不包含 API Key、企业内部数据或实时数据分析能力。

## 1. 创建 Knowledge

1. 登录 Dify 网页端。
2. 进入 Knowledge 模块，新建知识库。
3. 知识库名称建议使用：`淘宝用户行为分析项目知识库`。
4. 知识库说明可以写：用于回答淘宝用户行为与转化漏斗分析项目的背景、数据来源、指标口径、SQL 分析、业务洞察、看板设计和面试表达问题。

## 2. 上传项目文档

优先上传 Markdown 文档：

- `README.md`
- `reports/analysis_summary.md`
- `reports/business_insights.md`
- `reports/data_quality_report.md`
- `dashboard/dashboard_design.md`
- `sql/README.md`
- `PROJECT_SHARING_GUIDE.md`

如果使用 `dify_knowledge/` 中已整理好的资料包，可以上传对应的 `project_README.md`、`analysis_summary.md`、`business_insights.md`、`data_quality_report.md`、`dashboard_design.md`、`sql_README.md` 和 `project_sharing_guide.md`。

不要上传完整原始数据、压缩包、虚拟环境、缓存目录或 Excel 二进制文件。

## 3. 设置分块

推荐设置：

- Chunk size: 500-1024 characters
- Chunk overlap: 50-100 characters
- Retrieval mode: Semantic Search 或 Hybrid Search
- TopK: 3-5

上传后检查文档解析效果，确认中文、标题、表格和指标数值没有乱码或明显缺失。

## 4. 创建 Chatbot

1. 进入 Dify Studio。
2. 新建 Chatbot 应用。
3. 应用名称建议使用：`淘宝用户行为分析项目 AI 问答助手`。
4. 应用描述建议写：基于项目知识库回答数据分析项目背景、指标口径、业务洞察、看板设计和简历表达问题。

## 5. 绑定 Knowledge

在 Chatbot 配置中绑定刚创建的 Knowledge。检索策略优先保证准确性，如果回答缺少指标来源，可以适当调高 TopK；如果回答太发散，应检查系统提示词和知识库文档是否约束清晰。

## 6. 复制 system prompt

将 `dify_knowledge/system_prompt.md` 中的系统提示词复制到 Dify Chatbot 的 System Prompt 区域。重点保留以下约束：

- 优先基于知识库回答。
- 知识库没有相关信息时回答“根据当前项目文档无法确认”。
- 不编造不存在的数据、图表、API、线上链接或截图。
- 不把公开数据集样本夸大为企业内部真实数据。
- 不声称训练或微调了大模型。
- 谨慎区分用户级转化率和用户-商品级顺序转化率。

## 7. 开启 Citation / Attribution

建议开启 Citation / Attribution，让回答展示引用来源。这样在 GitHub 或面试演示时，可以说明答案来自 README、分析报告、业务洞察、SQL 说明或看板说明，而不是模型自由生成。

## 8. 测试关键问题

发布前建议测试：

- 为什么用户级转化率比用户-商品级顺序转化率高？
- 加购未购买用户有什么运营价值？
- 请用一分钟介绍这个项目。
- SQL 分析主要覆盖哪些问题？
- Excel 看板展示了哪些内容？

如果回答出现编造链接、混淆指标口径、夸大数据来源或声称实时分析 CSV，需要回到系统提示词和知识库文档中修正。

## 9. 发布 Web App

调试稳定后，可以在 Dify 中发布 Web App，并在 README 中放置公开可访问链接：

```text
https://udify.app/chat/0nIFW08DLfoL8IzA
```

发布后建议手动确认链接是否可公开访问。

## 10. 截图并更新 README

可以手动补充以下截图：

- `screenshots/dify_knowledge_files.png`：Dify 知识库文档列表。
- `screenshots/dify_chatbot_config.png`：Dify Chatbot 配置页面。
- `screenshots/dify_qa_demo.png`：Dify 问答效果演示。

只有当截图文件真实存在时，才在 README 中引用图片；不要创建或引用伪造截图。
