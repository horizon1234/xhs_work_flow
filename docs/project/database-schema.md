# 数据库表结构草案

这份文档保留“目标设计”的思路，但下面会先标注当前已经在代码里真正落地的表结构。

## 设计原则

1. 所有业务对象都要有状态字段
2. 所有生成结果都要保留来源关系
3. 所有核心内容都要支持版本化
4. 所有任务都要有审计字段

## 当前已落地表

### hotspots

用途：存储热点原始数据和聚合结果。

当前已实现字段：

- id
- source_type
- source_url
- keyword
- raw_title
- raw_content
- summary
- status
- created_at
- updated_at

### topic_candidates

用途：存储一个热点生成出的多个选题方向。

当前已实现字段：

- id
- hotspot_id
- angle_type
- title_hint
- description
- audience
- relevance_score
- risk_score
- status
- created_at
- updated_at

### copy_variants

用途：存储文案候选版本。

当前已实现字段：

- id
- topic_candidate_id
- model_name
- prompt_version
- title
- hook
- body
- hashtags
- cover_text
- comment_hint
- risk_notes
- status
- created_at
- updated_at

### review_tasks

用途：存储人工审核流程。

当前已实现字段：

- id
- hotspot_id
- topic_candidate_id
- copy_variant_id
- reviewer
- review_status
- review_notes
- created_at
- updated_at

## 当前关系说明

1. 一个 `hotspot` 可以生成多个 `topic_candidates`
2. 一个 `topic_candidate` 可以生成多个 `copy_variants`
3. 一个 `review_task` 可以关联热点，也可以进一步关联选题和文案
4. 当前审核状态会回写到热点、选题和文案对象本身

## 当前状态流转

当前代码已经实际使用的状态主要是：

1. collected
2. topic_generated
3. copy_generated
4. pending_review
5. approved
6. rejected

## 规划中的后续表

### image_assets

用途：存储封面、配图和导出素材。

规划字段：

- id
- copy_variant_id
- asset_type
- storage_path
- prompt_text
- width
- height
- style_name
- status
- created_at
- updated_at

### publish_tasks

用途：存储待发布和已发布记录。

规划字段：

- id
- review_task_id
- publish_status
- publish_mode
- publish_channel
- published_at
- failure_reason
- created_at
- updated_at

### performance_metrics

用途：存储发布后的内容表现。

规划字段：

- id
- publish_task_id
- impressions
- likes
- favorites
- comments
- shares
- collected_at
- created_at

### prompt_templates

用途：存储风格模板和版本。

规划字段：

- id
- template_type
- style_name
- version
- system_prompt
- user_prompt_template
- is_active
- created_at
- updated_at

## 目标态统一状态流转

建议统一状态：

1. collected
2. cleaned
3. topic_generated
4. copy_generated
5. image_generated
6. pending_review
7. approved
8. rejected
9. ready_to_publish
10. published
11. failed
12. archived
