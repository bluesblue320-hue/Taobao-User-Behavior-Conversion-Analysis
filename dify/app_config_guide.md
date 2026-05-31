# Dify App 配置说明

本说明用于在 Dify 网页端配置“淘宝用户行为分析 AI 问答助手”。这里只描述配置流程，不包含真实 API 调用、App ID、API Key 或线上链接。

## 1. 创建 Knowledge

1. 登录 Dify 网页端。
2. 进入 Knowledge 模块。
3. 新建知识库，建议命名为：`淘宝用户行为分析项目知识库`。
4. 知识库说明可以写：用于回答淘宝用户行为与转化漏斗分析项目的背景、指标、报告、看板和面试表达问题。

## 2. 上传建议文档

按照 `dify/knowledge_base_files.md` 中的清单上传项目文档，优先上传：

- `README.md`
- `reports/analysis_summary.md`
- `reports/business_insights.md`
- `reports/data_quality_report.md`
- `dashboard/dashboard_design.md`
- `sql/README.md`
- `PROJECT_SHARING_GUIDE.md`

上传后检查文档解析结果，确认标题、表格和段落没有明显乱码或缺失。

## 3. 创建 Chatbot 或 Chatflow

1. 进入 Dify Studio。
2. 新建应用，可以选择 Chatbot；如果希望后续加入更复杂的流程判断，再选择 Chatflow。
3. 应用名称建议使用：`淘宝用户行为分析 AI 问答助手`。
4. 应用描述建议写：基于项目知识库回答数据分析项目背景、指标口径、业务洞察、看板设计和简历表达问题。

## 4. 关联 Knowledge

1. 在应用配置中添加 Knowledge 检索节点或知识库检索能力。
2. 选择刚刚创建的项目知识库。
3. 检索策略建议优先保证回答准确性，可以选择较保守的 Top K 和相似度阈值。
4. 如果 Dify 支持重排模型，可以在可用条件下开启 rerank，以提高长文档检索质量。

## 5. 开启 Citation / Attribution

建议开启 citation / attribution，让回答展示引用来源。这样在面试演示时可以说明答案来自 README、分析报告或业务洞察文档，而不是模型自由生成。

## 6. 设置系统提示词

将 `dify/system_prompt.md` 中代码块里的系统提示词复制到 Dify 的 System Prompt 或 Chatflow 对应配置中。

重点确认以下约束已经保留：

- 回答必须基于项目知识库。
- 不确定时明确说明“不确定”。
- 不编造不存在的数据、链接、API Key 或线上应用。
- 谨慎解释用户级转化率和用户-商品级顺序转化率。
- 不能把公开样本夸大成企业内部真实生产数据。

## 7. 调试样例问题

使用 `dify/sample_questions.md` 中的问题进行调试。建议重点测试：

- 项目主要解决什么问题？
- 为什么用户级浏览-购买转化率比较高？
- 用户级转化率和用户-商品级顺序转化率有什么区别？
- 加购未购买用户有什么运营价值？
- 这个项目适合怎么写进简历？
- 面试时我应该怎么介绍这个项目？

如果回答出现编造链接、夸大数据来源或混淆指标口径，需要回到系统提示词和知识库文档中调整。

## 8. 发布 Web App

调试稳定后，可以在 Dify 中发布 Web App，用于作品集或面试演示。

发布后建议手动补充：

- Dify Web App 截图。
- 项目 README 中的演示入口说明。
- 如果确实公开部署，再补充真实 Web App 链接。

不要在仓库中提交 API Key 或任何敏感配置。

## 9. 可选：通过 API 接入 README 或前端页面

如果后续希望把 Dify 问答入口接入网页，可以使用 Dify API 或嵌入式 Web App。但本项目当前只提供配置说明，不实现 API 调用。

如需后续开发，建议：

- 使用环境变量保存 API Key。
- 不把密钥写入 README、前端代码或 Git 仓库。
- 在 README 中只展示配置思路、截图和真实可访问的公开链接。
- 明确说明这是个人作品集扩展功能，不是生产级企业系统。
