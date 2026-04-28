# 工作区

工作区负责把项目变成一套可执行工程，而不是停留在概念层。

建议阅读顺序：

1. [system-architecture.md](system-architecture.md)
2. [database-schema.md](database-schema.md)
3. [api-design.md](api-design.md)
4. [work-breakdown.md](work-breakdown.md)

## 工作区目标

构建一个 AI 图文内容生产系统的 V1，先完成“高质量半自动”，再逐步提升自动化程度。

## V1 范围

V1 默认不追求全自动发布，保留两个人工控制点：

1. 人工审核
2. 人工最终发布确认

这样可以显著降低：

1. 平台规则风险
2. 账号安全风险
3. 内容合规风险
4. AI 幻觉导致的事实风险
