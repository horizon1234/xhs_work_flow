# 工作区系统架构

## 项目目标

围绕一条完整内容链路构建系统：

1. 热点采集
2. 热点理解与选题
3. 文案生成
4. 图片生成
5. 审核工作台
6. 发布辅助
7. 数据回收与优化

## 当前系统现状

当前仓库已经实现的是一条“热点录入 -> 选题生成 -> 文案生成 -> 审核流转”的最小闭环。

已经落地的模块：

1. FastAPI 应用入口与总路由注册
2. 基于 SQLAlchemy 的 SQLite 持久化
3. 热点、选题、文案、审核任务四类核心实体
4. 模拟内容生成服务 `content_pipeline.py`
5. Next.js 前端审核工作台

尚未落地的模块：

1. 图片生成
2. 发布辅助
3. 热点自动采集
4. 数据分析回收

## 当前代码模块拆分

### 1. 应用与配置

职责：

- 创建 FastAPI 应用实例
- 挂载 API 路由
- 注册 CORS
- 启动时初始化数据库

对应目录：

- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/api/router.py`

### 2. 数据层

职责：

- 定义 ORM 基类
- 创建数据库引擎和会话
- 管理建表初始化
- 持久化热点、选题、文案、审核任务

对应目录：

- `backend/app/db/base.py`
- `backend/app/db/session.py`
- `backend/app/models/`

### 3. API 层

职责：

- 提供健康检查
- 提供热点录入与查询
- 提供选题生成与查询
- 提供文案生成与查询
- 提供审核任务创建、查询和审批流转

对应目录：

- `backend/app/api/routes/health.py`
- `backend/app/api/routes/hotspots.py`
- `backend/app/api/routes/topics.py`
- `backend/app/api/routes/review_tasks.py`

### 4. 服务层

职责：

- 基于热点构造选题候选
- 基于选题构造文案候选
- 统一承接后续接入真实 LLM 的位置

对应目录：

- `backend/app/services/content_pipeline.py`

### 5. 前端工作台

职责：

- 录入热点
- 查看热点、选题、文案和审核任务
- 触发选题生成、文案生成、送审、通过、驳回

对应目录：

- `frontend/app/page.js`
- `frontend/app/globals.css`

## 模块拆分

### 1. 热点采集模块

职责：

- 定时采集热点源
- 对标账号监控
- 热点去重和初步打分

输入：关键词池、账号池、外部热点源配置

输出：热点原始记录、摘要候选、热度指标

### 2. 选题引擎模块

职责：

- 提炼热点摘要
- 输出多个内容角度
- 给出账号适配分和风险分

### 3. 文案生成模块

职责：

- 生成标题
- 生成正文
- 生成标签
- 生成封面短句
- 生成评论区引导语

### 4. 图片生成模块

职责：

- 生成封面候选
- 生成配图候选
- 合成适配平台尺寸的最终图片

### 5. 审核工作台模块

职责：

- 查看热点原文
- 编辑 AI 生成文案
- 预览与替换图片
- 审核通过/驳回/重生成

### 6. 发布辅助模块

职责：

- 生成待发布任务
- 素材打包
- 半自动填写发布表单

### 7. 分析模块

职责：

- 回收内容表现数据
- 分析爆款规律
- 优化 Prompt 和选题策略

## 当前已实现链路图

```text
浏览器 / 前端工作台
  -> FastAPI API
  -> hotspots 表
  -> topic_candidates 表
  -> copy_variants 表
  -> review_tasks 表
  -> 前端审核操作
```

## 目标态 V1 架构图

```text
热点输入/热点采集
  -> 热点库
  -> 选题服务
  -> 文案生成服务
  -> 图片生成服务
  -> 审核队列
  -> 审核台
  -> 待发布队列
  -> 手动发布/半自动发布
```

## 当前技术选型

- Backend: FastAPI
- ORM: SQLAlchemy 2.x
- Database: SQLite（开发态）
- Frontend: Next.js

## 规划中的后续技术选型

- Database: PostgreSQL
- Cache/Queue: Redis
- Worker: Celery
- Automation: Playwright
- Image Processing: Pillow

## 非功能要求

1. 所有关键节点都要有状态机
2. 所有生成结果都要可追溯到输入来源
3. 所有发布结果都要有日志和审计记录
4. 高风险内容默认强制人工复核
