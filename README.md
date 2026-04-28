# XHS Work Flow

一个面向小红书图文账号的 AI 内容生产工作流仓库。

当前仓库按两个核心区域组织：

- 学习区：沉淀技术架构、学习路线和关键知识图谱
- 工作区：沉淀项目设计、接口设计、表结构和 V1 工程骨架

## 仓库目标

先完成一个可控的 V1：

1. 录入热点文本或链接
2. 生成选题、标题、正文候选
3. 生成封面与配图候选
4. 进入人工审核台
5. 审核通过后导出素材或进入半自动发布流程

后续再逐步补齐：

1. 热点自动采集
2. 排期与发布辅助
3. 数据回收和策略优化
4. 多账号与多风格支持

## 文档导航

### 学习区

- [docs/learning/README.md](docs/learning/README.md)
- [docs/learning/architecture.md](docs/learning/architecture.md)
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
	backend/                 FastAPI 后端骨架
	frontend/                审核台前端骨架
	docs/
		learning/              学习区文档
		project/               工作区文档
		daily-progress.md      每日工作与学习进度记录
	.gitignore
```

## V1 技术选型

- 后端：Python + FastAPI
- 数据库：PostgreSQL
- 缓存/队列：Redis
- 异步任务：Celery
- 自动化：Playwright
- 前端：Next.js
- 图像处理：Pillow
- 模型层：LLM API + 图像模型 API

## 当前阶段建议

按下面顺序推进：

1. 先读学习区文档，建立整体认知
2. 先完成后端文案生成链路
3. 再补封面生成模块
4. 再补审核台
5. 最后再接入热点采集和发布辅助

## 快速开始

### 后端

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```