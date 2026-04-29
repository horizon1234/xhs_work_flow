# 工作区

工作区负责把项目变成一套可执行工程，而不是停留在概念层。

建议阅读顺序：

1. [system-architecture.md](system-architecture.md)
2. [database-schema.md](database-schema.md)
3. [api-design.md](api-design.md)
4. [work-breakdown.md](work-breakdown.md)

## 工作区目标

构建一个 AI 图文内容生产系统的 V1，先完成“高质量半自动”，再逐步提升自动化程度。

## 当前已落地内容

当前仓库已经不只是设计草案，已经落地了一条可运行的最小链路：

1. 录入热点
2. 生成选题候选
3. 生成文案候选
4. 创建审核任务
5. 在前端工作台执行通过或驳回

对应新增代码主要集中在：

- `backend/app/db/`：SQLAlchemy Base、Engine、Session 和建表初始化
- `backend/app/models/`：`Hotspot`、`TopicCandidate`、`CopyVariant`、`ReviewTask`
- `backend/app/schemas/`：选题、文案、审核任务的请求响应结构
- `backend/app/api/routes/topics.py`：文案生成与文案查询接口
- `backend/app/services/content_pipeline.py`：模拟选题与文案生成逻辑
- `frontend/app/page.js`：热点到审核的三栏工作台
- `docs/learning/frontend-architecture.md`：前端架构学习文档

## 当前阅读建议

如果你的目标是先理解“代码已经做到哪一步”，建议按这个顺序看：

1. [system-architecture.md](system-architecture.md)
2. [api-design.md](api-design.md)
3. [database-schema.md](database-schema.md)
4. [work-breakdown.md](work-breakdown.md)

如果你的目标是补前端认知，再额外看：

1. [../learning/frontend-architecture.md](../learning/frontend-architecture.md)

## V1 范围

V1 默认不追求全自动发布，保留两个人工控制点：

1. 人工审核
2. 人工最终发布确认

这样可以显著降低：

1. 平台规则风险
2. 账号安全风险
3. 内容合规风险
4. AI 幻觉导致的事实风险

## 当前仍未完成的部分

下面这些内容仍然是工作区后续阶段，不是当前仓库已实现能力：

1. 图片生成与素材管理
2. 发布任务与发布辅助
3. 热点自动采集器
4. Redis / Celery 异步任务
5. 数据回收与策略优化面板
