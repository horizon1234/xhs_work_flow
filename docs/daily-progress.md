# 每日工作与学习进度

这个文档用于持续记录两条主线：

1. 学习进度
2. 项目进度

使用原则：

1. 每天只追加一条记录，不改历史结论
2. 每条记录尽量控制在 5 到 10 分钟内能写完
3. 先写结果，再写问题，最后写明天计划
4. 学习内容必须尽量映射到项目模块，避免只学不做

---

## 每日模板

复制下面这一段，追加到文档底部即可。

```md
## YYYY-MM-DD

### 今日目标

- 

### 今日完成

- 学习：
- 工作：

### 关键产出

- 文档：
- 代码：
- 结论：

### 遇到的问题

- 

### 解决方式

- 

### 当前进度判断

- 学习进度：
- 项目进度：

### 明日计划

- 

### 备注

- 
```

---

## 2026-04-28

### 今日目标

- 搭建这个项目的长期文档基础
- 明确学习区和工作区的边界
- 建立可继续迭代的 V1 工程骨架

### 今日完成

- 学习：
  - 梳理了项目的完整业务链路，包括热点采集、选题生成、文案生成、图片生成、审核、发布和数据回收
  - 明确了 V1 不追求全自动发布，而是优先做人审可控闭环
- 工作：
  - 新增学习区文档，沉淀技术架构和 12 周学习路线
  - 新增工作区文档，沉淀系统架构、数据库草案、API 草案和实施拆解
  - 搭建 FastAPI 后端骨架
  - 搭建 Next.js 前端骨架
  - 新增热点与审核任务的占位接口

### 关键产出

- 文档：
  - docs/learning/README.md
  - docs/learning/architecture.md
  - docs/learning/roadmap-12-weeks.md
  - docs/project/README.md
  - docs/project/system-architecture.md
  - docs/project/database-schema.md
  - docs/project/api-design.md
  - docs/project/work-breakdown.md
- 代码：
  - backend/app/main.py
  - backend/app/api/router.py
  - backend/app/api/routes/health.py
  - backend/app/api/routes/hotspots.py
  - backend/app/api/routes/review_tasks.py
  - frontend/app/page.js
- 结论：
  - 当前最合理的推进顺序是：后端业务骨架 -> 数据模型 -> 文案生成 -> 图片生成 -> 审核台 -> 采集器 -> 发布辅助

### 遇到的问题

- 后端环境最开始没有安装 FastAPI 依赖，编辑器报了导入错误
- 项目初始阶段很容易目标过大，直接追求全自动会导致设计失控

### 解决方式

- 已配置 Python 虚拟环境并安装最小后端依赖
- 已通过文档把 V1 范围收敛为“热点录入到审核出稿”的闭环

### 当前进度判断

- 学习进度：已完成整体认知搭建，下一步进入后端、数据库和 LLM 接入的实操阶段
- 项目进度：已完成仓库初始化、文档体系和前后端基础骨架，进入 V1 核心功能开发前期

### 明日计划

- 补充数据库模型和 SQLAlchemy 结构
- 补充热点录入到审核任务创建的主流程
- 为文案生成模块设计输入输出结构

### 备注

- 以后每天优先更新这个文档，再开始当天开发
- 每周可基于每日记录再整理一份周总结

---

## 2026-04-29

### 今日目标

- 把后端从占位接口推进到真实持久化工作流
- 打通热点到审核的最小闭环
- 同步更新仓库文档，避免设计文档落后于代码

### 今日完成

- 学习：
  - 梳理了 SQLAlchemy 2.x 在当前项目里的最小落地方式，包括 Base、Session、Model 和建表初始化
  - 梳理了 Next.js 单页工作台如何通过 `fetch` 直接驱动 FastAPI 工作流
- 工作：
  - 新增数据库层 `db/base.py`、`db/session.py`
  - 新增四个核心模型：`Hotspot`、`TopicCandidate`、`CopyVariant`、`ReviewTask`
  - 新增选题与文案相关 schema
  - 新增 `topics.py` 路由，打通文案生成与查询
  - 新增 `content_pipeline.py`，实现模拟选题和文案生成
  - 将热点和审核任务接口从内存占位改为数据库持久化
  - 为审核任务补充通过和驳回动作
  - 将前端首页改造成热点录入、选题生成、文案生成、审核处理三栏工作台
  - 新增前端架构学习文档，并补齐工作区文档和前端说明文档

### 关键产出

- 文档：
  - docs/learning/frontend-architecture.md
  - docs/learning/笔记.md
  - docs/project/README.md
  - docs/project/system-architecture.md
  - docs/project/api-design.md
  - docs/project/database-schema.md
  - docs/project/work-breakdown.md
  - docs/daily-progress.md
- 代码：
  - backend/app/db/base.py
  - backend/app/db/session.py
  - backend/app/models/__init__.py
  - backend/app/models/hotspot.py
  - backend/app/models/topic_candidate.py
  - backend/app/models/copy_variant.py
  - backend/app/models/review_task.py
  - backend/app/api/routes/topics.py
  - backend/app/services/content_pipeline.py
  - frontend/app/page.js
- 结论：
  - 项目已经从“文档 + 骨架”阶段进入“热点到审核最小闭环可演示”阶段

### 遇到的问题

- 工作区文档仍然停留在早期草案，和当前代码状态出现偏差
- 前端说明文档没有覆盖新的三栏工作台和运行方式
- 学习笔记文件已创建但还没有内容，无法承接当天的认知沉淀

### 解决方式

- 全局检索 git 新增文件，对照现有 Markdown 逐项补齐
- 把文档表述从“计划要做”改成“当前已实现 + 后续待补”
- 追加当日日报，记录新增模块和阶段判断

### 当前进度判断

- 学习进度：已从概念理解进入框架级实操，下一步要进入真实 LLM、异步任务和前端拆分
- 项目进度：最小闭环已跑通，下一阶段重点是增强生成质量、补图片资产和引入异步工作流

### 明日计划

- 为 mock 内容生成链路设计真实 LLM 接入接口
- 评估图片资产表和图片生成接口的最小实现方式
- 继续整理前后端拆分边界，减少首页和路由文件继续膨胀

### 备注

- 后续每次新增文件后，都应该同步检查工作区文档是否仍然准确
- 当前数据库为开发态 SQLite，后续如进入多环境部署，再切换到 PostgreSQL