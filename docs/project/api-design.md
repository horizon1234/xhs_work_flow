# API 设计草案

下面分成两部分：

1. 当前仓库已经实现的接口
2. 后续规划中的接口

## 设计原则

1. V1 优先以审核台和内容生成链路为中心
2. 接口返回结构化 JSON
3. 所有长任务都支持异步化和状态查询

## 主要资源

- hotspots
- topic-candidates
- copy-variants
- image-assets
- review-tasks
- publish-tasks

## 当前已实现接口

### 健康检查

- GET /api/v1/health

### 热点录入与查询

- POST /api/v1/hotspots
- GET /api/v1/hotspots
- GET /api/v1/hotspots/{hotspot_id}

请求示例：

```json
{
  "source_type": "manual",
  "source_url": "https://example.com/topic",
  "keyword": "职场热点",
  "raw_title": "某热点标题",
  "raw_content": "热点正文或摘要"
}
```

返回要点：

- 热点会落库，不再是内存占位
- 返回结构中包含 `id`、`summary`、`status`

### 选题生成

- POST /api/v1/hotspots/{hotspot_id}/generate-topics
- GET /api/v1/hotspots/{hotspot_id}/topics

说明：

- 如果该热点已经生成过选题，再次调用生成接口会直接返回已有选题
- 当前由 `content_pipeline.py` 返回模拟选题候选

### 文案生成

- POST /api/v1/topics/{topic_id}/generate-copy
- GET /api/v1/topics/{topic_id}/copy-variants

说明：

- 当前文案由 mock pipeline 生成
- 返回字段包含标题、hook、正文、hashtags、封面短句和风险提示

### 审核流转

- POST /api/v1/review-tasks
- GET /api/v1/review-tasks
- GET /api/v1/review-tasks/{review_task_id}
- POST /api/v1/review-tasks/{review_task_id}/approve
- POST /api/v1/review-tasks/{review_task_id}/reject

审核任务创建说明：

- `hotspot_id`、`topic_candidate_id`、`copy_variant_id` 至少传一个
- 如果只传 `copy_variant_id`，后端会自动反向解析所属选题和热点

审批动作请求示例：

```json
{
  "reviewer": "operator",
  "review_notes": "观点可用，但发布前需要补事实核验"
}
```

状态流转说明：

- 审核通过后，关联的热点、选题、文案状态会同步更新为 `approved`
- 审核驳回后，关联状态会同步更新为 `rejected`

## 当前接口优先级完成情况

已完成：

1. health
2. hotspots 创建、列表、详情
3. generate-topics 和 topics 列表
4. generate-copy 和 copy-variants 列表
5. review-tasks 创建、列表、详情
6. approve 和 reject

## 后续规划接口

### 图片生成

- POST /api/v1/copy-variants/{copy_variant_id}/generate-images
- GET /api/v1/copy-variants/{copy_variant_id}/images

### 发布任务

- POST /api/v1/publish-tasks
- GET /api/v1/publish-tasks
- POST /api/v1/publish-tasks/{publish_task_id}/prepare
