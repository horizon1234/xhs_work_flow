# 数据库表结构草案

## 设计原则

1. 所有业务对象都要有状态字段
2. 所有生成结果都要保留来源关系
3. 所有核心内容都要支持版本化
4. 所有任务都要有审计字段

## 核心表

### hotspots

用途：存储热点原始数据和聚合结果。

建议字段：

- id
- source_type
- source_url
- source_author
- keyword
- raw_title
- raw_content
- summary
- heat_score
- relevance_score
- risk_score
- status
- collected_at
- created_at
- updated_at

### topic_candidates

用途：存储一个热点生成出的多个选题方向。

建议字段：

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

建议字段：

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

### image_assets

用途：存储封面、配图和导出素材。

建议字段：

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

### review_tasks

用途：存储人工审核流程。

建议字段：

- id
- hotspot_id
- topic_candidate_id
- copy_variant_id
- selected_cover_asset_id
- reviewer
- review_status
- review_notes
- scheduled_publish_at
- created_at
- updated_at

### publish_tasks

用途：存储待发布和已发布记录。

建议字段：

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

建议字段：

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

建议字段：

- id
- template_type
- style_name
- version
- system_prompt
- user_prompt_template
- is_active
- created_at
- updated_at

## 核心状态流转

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
