# API 设计草案

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

## 接口草案

### 健康检查

- GET /api/v1/health

### 热点录入与查询

- POST /api/v1/hotspots
- GET /api/v1/hotspots
- GET /api/v1/hotspots/{hotspot_id}

请求示例：

```json
{
  "sourceType": "manual",
  "sourceUrl": "https://example.com/topic",
  "keyword": "职场热点",
  "rawTitle": "某热点标题",
  "rawContent": "热点正文或摘要"
}
```

### 选题生成

- POST /api/v1/hotspots/{hotspot_id}/generate-topics
- GET /api/v1/hotspots/{hotspot_id}/topics

### 文案生成

- POST /api/v1/topics/{topic_id}/generate-copy
- GET /api/v1/topics/{topic_id}/copy-variants

### 图片生成

- POST /api/v1/copy-variants/{copy_variant_id}/generate-images
- GET /api/v1/copy-variants/{copy_variant_id}/images

### 审核流转

- POST /api/v1/review-tasks
- GET /api/v1/review-tasks
- GET /api/v1/review-tasks/{review_task_id}
- POST /api/v1/review-tasks/{review_task_id}/approve
- POST /api/v1/review-tasks/{review_task_id}/reject

### 发布任务

- POST /api/v1/publish-tasks
- GET /api/v1/publish-tasks
- POST /api/v1/publish-tasks/{publish_task_id}/prepare

## V1 接口优先级

第一批必须完成：

1. health
2. hotspots 创建与列表
3. generate-topics
4. generate-copy
5. review-tasks 创建与查询

第二批补充：

1. generate-images
2. approve/reject
3. publish-tasks
