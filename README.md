# XHS Work Flow

一个面向小红书图文账号的 AI 内容生产工作流仓库。

当前仓库按两个核心区域组织：

- 学习区：沉淀技术架构、学习路线和关键知识图谱
- 工作区：沉淀项目设计、接口设计、表结构和 V1 工程骨架

当前已经落地的是一条可演示的最小闭环：

1. 录入热点
2. 生成选题候选
3. 生成文案候选
4. 创建审核任务
5. 在前端工作台执行通过 / 驳回

## 仓库目标

先完成一个可控的 V1：

1. 录入热点文本或链接
2. 生成选题、标题、正文候选
3. 进入人工审核台
4. 审核通过后导出素材或进入半自动发布流程
5. 再逐步扩展封面、配图和发布辅助能力

后续再逐步补齐：

1. 热点自动采集
2. 排期与发布辅助
3. 数据回收和策略优化
4. 多账号与多风格支持

## 文档导航

### 学习区

- [docs/learning/README.md](docs/learning/README.md)
- [docs/learning/architecture.md](docs/learning/architecture.md)
- [docs/learning/笔记.md](docs/learning/笔记.md)
- [docs/learning/roadmap-12-weeks.md](docs/learning/roadmap-12-weeks.md)
- [docs/daily-progress.md](docs/daily-progress.md)

### 工作区

- [docs/project/README.md](docs/project/README.md)
- [docs/project/system-architecture.md](docs/project/system-architecture.md)
- [docs/project/database-schema.md](docs/project/database-schema.md)
- [docs/project/api-design.md](docs/project/api-design.md)
- [docs/project/work-breakdown.md](docs/project/work-breakdown.md)

## 目录结构

```text
xhs_work_flow/
	backend/                 FastAPI + SQLAlchemy 后端工作流
	frontend/                Next.js 审核工作台
	docs/
		learning/              学习区文档
		project/               工作区文档
		daily-progress.md      每日工作与学习进度记录
	.gitignore
```

## 当前实现快照

后端已完成：

1. FastAPI 应用入口、路由注册、CORS 配置
2. SQLAlchemy 会话管理与 SQLite 建表初始化
3. `hotspots`、`topic_candidates`、`copy_variants`、`review_tasks` 四类核心模型
4. 热点录入、选题生成、文案生成、审核任务创建与审批接口
5. 基于 `content_pipeline.py` 的模拟内容生成逻辑

前端已完成：

1. 热点录入表单
2. 热点列表与当前焦点区
3. 选题候选列表
4. 文案候选与送审操作
5. 审核任务列表与通过 / 驳回操作

## 当前技术栈

- 后端：Python + FastAPI
- ORM：SQLAlchemy 2.x
- 配置：pydantic-settings
- 数据库：SQLite（开发态）
- 前端：Next.js 15 + React 19
- 内容生成：本地 mock pipeline，后续可替换为真实 LLM

## 当前阶段建议

按下面顺序推进：

1. 先读学习区文档，建立整体认知
2. 先把热点 -> 选题 -> 文案 -> 审核链路跑通
3. 再补真实 LLM、图片生成和素材存储
4. 再接入热点采集、任务调度和发布辅助
5. 最后补数据回收和策略优化

## 快速开始

### 后端

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Windows PowerShell 可以改成：

```powershell
.venv\Scripts\Activate.ps1
```

启动后默认访问：

- Swagger 文档：`http://127.0.0.1:8000/docs`
- API 前缀：`http://127.0.0.1:8000/api/v1`

### 前端

```bash
export PATH=/home/zyh/.local/node-v20.19.0-linux-x64/bin:$PATH
cd frontend
npm install
npm run dev
```

如需连接非默认后端地址，可以设置环境变量：

```bash
export NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## 当前未完成部分

下面这些仍处于设计或预留阶段：

1. 图片生成与素材资产管理
2. 发布任务与发布辅助
3. Redis / Celery 异步任务
4. 热点自动采集器
5. 真实大模型接入与 Prompt 模板管理