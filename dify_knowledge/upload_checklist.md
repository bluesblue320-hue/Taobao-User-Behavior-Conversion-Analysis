# Dify Knowledge 上传清单

## 建议上传文件清单

建议优先上传以下 Markdown 文件到 Dify Knowledge：

- `dify_knowledge/project_README.md`
- `dify_knowledge/analysis_summary.md`
- `dify_knowledge/business_insights.md`
- `dify_knowledge/data_quality_report.md`
- `dify_knowledge/dashboard_design.md`
- `dify_knowledge/sql_README.md`
- `dify_knowledge/project_sharing_guide.md`

可选上传：

- `dify_knowledge/README.md`：如果希望助手也能回答“知识库资料包包含什么”这类问题，可以上传。

不建议上传到 Knowledge：

- `dify_knowledge/system_prompt.md`：建议复制到 Dify Chatbot / Chatflow 的系统提示词区域。
- `dify_knowledge/sample_questions.md`：建议作为人工测试问题保留。
- `dify_knowledge/upload_checklist.md`：建议作为上传前操作清单保留。
- `data/UserBehavior.csv`
- `data/UserBehavior.csv.zip`
- `data/*.zip`
- `.venv/`
- `__pycache__/`
- `node_modules/`
- `*.pyc`
- `dashboard/*.xlsx`
- 大体积原始数据文件

## 上传前检查项

- 确认上传文件均为 Markdown 文档，且内容能正常显示中文。
- 确认没有上传完整原始大数据文件，例如 `data/UserBehavior.csv`、`data/UserBehavior.csv.zip` 或 `data/*.zip`。
- 确认没有上传虚拟环境、缓存目录或依赖目录，例如 `.venv/`、`__pycache__/`、`node_modules/`、`*.pyc`。
- 确认项目表述为公开数据集样本分析和个人作品集项目，不表述为企业内部真实生产系统。
- 确认核心指标数值与报告一致，不在 Dify 中手动改写指标。
- 确认 `system_prompt.md` 已复制到 Dify 的系统提示词区域，而不是只作为普通知识文档上传。
- 上传后用测试问题检查 Citation / Attribution 是否能引用到对应文档。

## Dify 分块建议

- Chunk size: 500-1024 characters
- Chunk overlap: 50-100 characters
- Retrieval mode: Semantic Search 或 Hybrid Search
- TopK: 3-5
- 开启 Citation / Attribution

如果问答经常漏掉指标表格，可适当降低 Chunk size 或启用 Hybrid Search；如果回答过于碎片化，可适当提高 Chunk size。

## Dify 检索测试问题

上传后建议至少测试以下问题：

1. 这个项目的数据来源是什么，样本规模是多少？
2. 数据清洗后为什么从 100,000 行变成 99,956 行？
3. 用户级浏览-购买转化率和用户-商品级顺序浏览-购买转化率有什么区别？
4. 本项目的复购率是多少，应该如何解释？
5. 加购未购买用户有多少，适合做什么运营动作？
6. SQL 分析覆盖了哪些查询场景？
7. Excel 看板包含哪些页面和核心 KPI？
8. 如果面试官问这个项目的业务价值，应该怎么回答？
9. 为什么用户级转化率比用户-商品级顺序转化率高？
10. 请用一分钟介绍这个项目。

检查标准：

- 回答应能引用对应知识库文档。
- 涉及指标时应给出明确口径和限制。
- 知识库没有的信息应回答“不确定”，不能编造线上链接、API、图表或企业内部背景。
