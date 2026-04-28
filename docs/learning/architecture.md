# 学习区技术架构图

## 目标视角

这个项目不是单点工具，而是一条内容生产流水线：

1. 发现热点
2. 理解热点
3. 生成选题
4. 生成文案
5. 生成封面与配图
6. 人工审核
7. 发布执行
8. 数据回收与优化

## 分层架构

### 1. 业务层

- 热点采集
- 热点清洗
- 选题生成
- 文案生成
- 图片生成
- 审核流转
- 发布辅助
- 数据分析

### 2. 服务层

- crawler-service
- topic-service
- copywriting-service
- image-service
- review-service
- publishing-service
- analytics-service

### 3. 基础能力层

- FastAPI
- PostgreSQL
- Redis
- Celery
- Playwright
- LLM API
- Image API
- Object Storage

### 4. 运维保障层

- 日志
- 告警
- 审计
- 重试
- 幂等
- 配置管理

## 知识图谱

### 第一阶段必须掌握

1. Python 工程化
2. FastAPI
3. SQLAlchemy
4. PostgreSQL
5. Redis
6. Playwright
7. LLM API 调用
8. Prompt 设计
9. Docker

### 第二阶段逐步补齐

1. Celery
2. RAG
3. 向量检索
4. 图像生成
5. OCR
6. 数据分析
7. 内容安全

### 第三阶段优化增强

1. 多账号支持
2. 成本控制
3. 自动策略调优
4. 爆款特征归因

## 学习优先级原则

优先顺序不是“最酷”，而是“最能支撑 V1 交付”：

1. 先把后端、文案生成、审核流转做通
2. 再加图片生成
3. 再加热点采集
4. 最后再做发布自动化和数据闭环
