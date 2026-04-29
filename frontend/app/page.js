'use client'

import { startTransition, useEffect, useMemo, useState } from 'react'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://127.0.0.1:8000/api/v1'

const initialHotspotForm = {
  source_type: 'manual',
  source_url: '',
  keyword: '',
  raw_title: '',
  raw_content: '',
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  })

  if (!response.ok) {
    let message = `Request failed: ${response.status}`
    try {
      const payload = await response.json()
      message = payload.detail ?? message
    } catch {}
    throw new Error(message)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

function StatCard({ label, value, tone = 'default' }) {
  return (
    <article className={`stat-card stat-card--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  )
}

function EmptyState({ title, detail, action }) {
  return (
    <div className="empty-state">
      <strong>{title}</strong>
      <p>{detail}</p>
      {action}
    </div>
  )
}

export default function HomePage() {
  const [hotspotForm, setHotspotForm] = useState(initialHotspotForm)
  const [reviewer, setReviewer] = useState('operator')
  const [notesByKey, setNotesByKey] = useState({})
  const [hotspots, setHotspots] = useState([])
  const [topics, setTopics] = useState([])
  const [copyVariants, setCopyVariants] = useState([])
  const [reviewTasks, setReviewTasks] = useState([])
  const [selectedHotspotId, setSelectedHotspotId] = useState(null)
  const [selectedTopicId, setSelectedTopicId] = useState(null)
  const [statusMessage, setStatusMessage] = useState('正在连接后端工作流...')
  const [errorMessage, setErrorMessage] = useState('')
  const [busyKey, setBusyKey] = useState('')

  const selectedHotspot = hotspots.find((item) => item.id === selectedHotspotId) ?? null
  const selectedTopic = topics.find((item) => item.id === selectedTopicId) ?? null

  const stats = useMemo(() => {
    const pendingCount = reviewTasks.filter((task) => task.review_status === 'pending_review').length
    const approvedCount = reviewTasks.filter((task) => task.review_status === 'approved').length
    const rejectedCount = reviewTasks.filter((task) => task.review_status === 'rejected').length

    return {
      hotspotCount: hotspots.length,
      pendingCount,
      approvedCount,
      rejectedCount,
    }
  }, [hotspots, reviewTasks])

  async function loadHotspots(preferredHotspotId) {
    const data = await request('/hotspots')
    startTransition(() => {
      setHotspots(data)
      if (data.length === 0) {
        setSelectedHotspotId(null)
        return
      }

      const nextHotspotId =
        preferredHotspotId ??
        (data.some((item) => item.id === selectedHotspotId) ? selectedHotspotId : data[0].id)
      setSelectedHotspotId(nextHotspotId)
    })
    return data
  }

  async function loadTopics(hotspotId, preferredTopicId) {
    if (!hotspotId) {
      startTransition(() => {
        setTopics([])
        setCopyVariants([])
        setSelectedTopicId(null)
      })
      return []
    }

    const data = await request(`/hotspots/${hotspotId}/topics`)
    startTransition(() => {
      setTopics(data)
      if (data.length === 0) {
        setSelectedTopicId(null)
        setCopyVariants([])
        return
      }

      const nextTopicId =
        preferredTopicId ?? (data.some((item) => item.id === selectedTopicId) ? selectedTopicId : data[0].id)
      setSelectedTopicId(nextTopicId)
    })
    return data
  }

  async function loadCopyVariants(topicId) {
    if (!topicId) {
      startTransition(() => setCopyVariants([]))
      return []
    }

    const data = await request(`/topics/${topicId}/copy-variants`)
    startTransition(() => setCopyVariants(data))
    return data
  }

  async function loadReviewTasks() {
    const data = await request('/review-tasks')
    startTransition(() => setReviewTasks(data))
    return data
  }

  async function refreshWorkspace({ hotspotId = selectedHotspotId, topicId = selectedTopicId } = {}) {
    setErrorMessage('')
    const hotspotData = await loadHotspots(hotspotId)
    const resolvedHotspotId = hotspotId ?? hotspotData[0]?.id ?? null
    const topicData = await loadTopics(resolvedHotspotId, topicId)
    const resolvedTopicId = topicId ?? topicData[0]?.id ?? null
    await Promise.all([loadCopyVariants(resolvedTopicId), loadReviewTasks()])
    setStatusMessage('工作台已同步到最新状态。')
  }

  useEffect(() => {
    refreshWorkspace().catch((error) => {
      setErrorMessage(error.message)
      setStatusMessage('后端未连接，请先启动 FastAPI 服务。')
    })
  }, [])

  useEffect(() => {
    if (!selectedHotspotId) {
      return
    }

    loadTopics(selectedHotspotId)
      .then((topicData) => loadCopyVariants(topicData[0]?.id ?? null))
      .catch((error) => setErrorMessage(error.message))
  }, [selectedHotspotId])

  useEffect(() => {
    if (!selectedTopicId) {
      return
    }

    loadCopyVariants(selectedTopicId).catch((error) => setErrorMessage(error.message))
  }, [selectedTopicId])

  async function runAction(actionKey, task) {
    setBusyKey(actionKey)
    setErrorMessage('')

    try {
      await task()
    } catch (error) {
      setErrorMessage(error.message)
    } finally {
      setBusyKey('')
    }
  }

  async function handleCreateHotspot(event) {
    event.preventDefault()

    await runAction('create-hotspot', async () => {
      const payload = {
        ...hotspotForm,
        source_url: hotspotForm.source_url || undefined,
      }
      const hotspot = await request('/hotspots', {
        method: 'POST',
        body: JSON.stringify(payload),
      })

      setHotspotForm(initialHotspotForm)
      await refreshWorkspace({ hotspotId: hotspot.id, topicId: null })
      setStatusMessage(`已创建热点 #${hotspot.id}，可以继续生成选题。`)
    })
  }

  async function handleGenerateTopics() {
    if (!selectedHotspotId) {
      return
    }

    await runAction('generate-topics', async () => {
      const generatedTopics = await request(`/hotspots/${selectedHotspotId}/generate-topics`, {
        method: 'POST',
        body: JSON.stringify({}),
      })

      startTransition(() => {
        setTopics(generatedTopics)
        setSelectedTopicId(generatedTopics[0]?.id ?? null)
      })
      await loadHotspots(selectedHotspotId)
      await loadCopyVariants(generatedTopics[0]?.id ?? null)
      setStatusMessage(`热点 #${selectedHotspotId} 已生成 ${generatedTopics.length} 个选题。`)
    })
  }

  async function handleGenerateCopy(topicId) {
    await runAction(`generate-copy-${topicId}`, async () => {
      const generatedCopy = await request(`/topics/${topicId}/generate-copy`, {
        method: 'POST',
        body: JSON.stringify({}),
      })

      startTransition(() => {
        setSelectedTopicId(topicId)
        setCopyVariants(generatedCopy)
      })
      await loadHotspots(selectedHotspotId)
      await loadTopics(selectedHotspotId, topicId)
      setStatusMessage(`选题 #${topicId} 已生成 ${generatedCopy.length} 条文案。`)
    })
  }

  async function handleCreateReviewTask(copyVariantId) {
    await runAction(`create-review-${copyVariantId}`, async () => {
      const reviewTask = await request('/review-tasks', {
        method: 'POST',
        body: JSON.stringify({
          copy_variant_id: copyVariantId,
          reviewer: reviewer || undefined,
          review_notes: notesByKey[`copy-${copyVariantId}`] || undefined,
        }),
      })

      await refreshWorkspace({ hotspotId: selectedHotspotId, topicId: selectedTopicId })
      setStatusMessage(`审核任务 #${reviewTask.id} 已创建，等待处理。`)
    })
  }

  async function handleReviewDecision(reviewTaskId, action) {
    await runAction(`${action}-${reviewTaskId}`, async () => {
      const reviewTask = await request(`/review-tasks/${reviewTaskId}/${action}`, {
        method: 'POST',
        body: JSON.stringify({
          reviewer: reviewer || undefined,
          review_notes: notesByKey[`task-${reviewTaskId}`] || undefined,
        }),
      })

      await refreshWorkspace({ hotspotId: reviewTask.hotspot_id, topicId: reviewTask.topic_candidate_id })
      setStatusMessage(`审核任务 #${reviewTask.id} 已更新为 ${reviewTask.review_status}。`)
    })
  }

  return (
    <main className="page-shell dashboard-shell">
      <section className="hero hero--dashboard">
        <div>
          <p className="eyebrow">XHS Workflow Console</p>
          <h1>热点到审核的最小工作台</h1>
          <p className="lead">
            这一版直接连现有 FastAPI 接口，先把热点录入、选题生成、文案生成、人工审核状态流转跑通。
          </p>
        </div>

        <div className="hero-meta">
          <label className="field-label" htmlFor="reviewer">
            当前审核人
          </label>
          <input
            id="reviewer"
            className="text-input"
            value={reviewer}
            onChange={(event) => setReviewer(event.target.value)}
            placeholder="输入审核人名称"
          />
          <p className="status-line">API: {API_BASE_URL}</p>
        </div>
      </section>

      <section className="stats-grid">
        <StatCard label="热点总数" value={stats.hotspotCount} />
        <StatCard label="待审核" value={stats.pendingCount} tone="warning" />
        <StatCard label="已通过" value={stats.approvedCount} tone="success" />
        <StatCard label="已驳回" value={stats.rejectedCount} tone="danger" />
      </section>

      <section className="message-bar">
        <p>{statusMessage}</p>
        {errorMessage ? <p className="message-bar__error">{errorMessage}</p> : null}
      </section>

      <section className="workspace-grid">
        <aside className="panel stack-panel">
          <div className="panel-header">
            <div>
              <p className="section-kicker">录入</p>
              <h2>新建热点</h2>
            </div>
          </div>

          <form className="stack-form" onSubmit={handleCreateHotspot}>
            <label className="field">
              <span className="field-label">关键词</span>
              <input
                className="text-input"
                value={hotspotForm.keyword}
                onChange={(event) => setHotspotForm((current) => ({ ...current, keyword: event.target.value }))}
                placeholder="例如：职场趋势"
                required
              />
            </label>

            <label className="field">
              <span className="field-label">标题</span>
              <input
                className="text-input"
                value={hotspotForm.raw_title}
                onChange={(event) => setHotspotForm((current) => ({ ...current, raw_title: event.target.value }))}
                placeholder="输入热点标题"
                required
              />
            </label>

            <label className="field">
              <span className="field-label">来源链接</span>
              <input
                className="text-input"
                value={hotspotForm.source_url}
                onChange={(event) => setHotspotForm((current) => ({ ...current, source_url: event.target.value }))}
                placeholder="可选"
                type="url"
              />
            </label>

            <label className="field">
              <span className="field-label">摘要正文</span>
              <textarea
                className="text-area"
                value={hotspotForm.raw_content}
                onChange={(event) => setHotspotForm((current) => ({ ...current, raw_content: event.target.value }))}
                placeholder="输入热点摘要或正文"
                rows={6}
                required
              />
            </label>

            <button className="button button--primary" disabled={busyKey === 'create-hotspot'} type="submit">
              {busyKey === 'create-hotspot' ? '创建中...' : '创建热点'}
            </button>
          </form>

          <div className="panel-header panel-header--list">
            <div>
              <p className="section-kicker">热点池</p>
              <h2>最近录入</h2>
            </div>
            <button className="button button--ghost" onClick={() => refreshWorkspace()} type="button">
              刷新
            </button>
          </div>

          <div className="stack-list">
            {hotspots.length === 0 ? (
              <EmptyState title="还没有热点" detail="先创建一条热点，工作流才会开始滚动。" />
            ) : (
              hotspots.map((hotspot) => (
                <button
                  key={hotspot.id}
                  className={`list-card ${selectedHotspotId === hotspot.id ? 'is-active' : ''}`}
                  onClick={() => setSelectedHotspotId(hotspot.id)}
                  type="button"
                >
                  <div className="list-card__meta">
                    <span>#{hotspot.id}</span>
                    <span className={`pill pill--${hotspot.status}`}>{hotspot.status}</span>
                  </div>
                  <strong>{hotspot.raw_title}</strong>
                  <p>{hotspot.summary ?? hotspot.raw_content}</p>
                </button>
              ))
            )}
          </div>
        </aside>

        <section className="panel main-panel">
          <div className="panel-header">
            <div>
              <p className="section-kicker">工作区</p>
              <h2>{selectedHotspot ? selectedHotspot.raw_title : '选择一个热点'}</h2>
            </div>
            <button
              className="button button--primary"
              disabled={!selectedHotspotId || busyKey === 'generate-topics'}
              onClick={handleGenerateTopics}
              type="button"
            >
              {busyKey === 'generate-topics' ? '生成中...' : '生成选题'}
            </button>
          </div>

          {selectedHotspot ? (
            <article className="focus-card">
              <div className="focus-card__meta">
                <span>关键词：{selectedHotspot.keyword}</span>
                <span className={`pill pill--${selectedHotspot.status}`}>{selectedHotspot.status}</span>
              </div>
              <p>{selectedHotspot.raw_content}</p>
            </article>
          ) : (
            <EmptyState title="没有选中的热点" detail="左侧选择热点后，就能生成选题与文案。" />
          )}

          <div className="content-grid">
            <section className="sub-panel">
              <div className="panel-header panel-header--tight">
                <div>
                  <p className="section-kicker">选题</p>
                  <h3>候选切角</h3>
                </div>
              </div>

              <div className="stack-list">
                {topics.length === 0 ? (
                  <EmptyState
                    title="还没有选题"
                    detail="先为当前热点生成选题。"
                    action={
                      <button className="button button--ghost" onClick={handleGenerateTopics} type="button">
                        立即生成
                      </button>
                    }
                  />
                ) : (
                  topics.map((topic) => (
                    <button
                      key={topic.id}
                      className={`list-card ${selectedTopicId === topic.id ? 'is-active' : ''}`}
                      onClick={() => setSelectedTopicId(topic.id)}
                      type="button"
                    >
                      <div className="list-card__meta">
                        <span>{topic.angle_type}</span>
                        <span className={`pill pill--${topic.status}`}>{topic.status}</span>
                      </div>
                      <strong>{topic.title_hint}</strong>
                      <p>{topic.description}</p>
                      <div className="metric-row">
                        <span>相关度 {topic.relevance_score}</span>
                        <span>风险 {topic.risk_score}</span>
                      </div>
                    </button>
                  ))
                )}
              </div>
            </section>

            <section className="sub-panel">
              <div className="panel-header panel-header--tight">
                <div>
                  <p className="section-kicker">文案</p>
                  <h3>{selectedTopic ? '候选文案' : '先选中一个选题'}</h3>
                </div>
                <button
                  className="button button--ghost"
                  disabled={!selectedTopicId || busyKey === `generate-copy-${selectedTopicId}`}
                  onClick={() => handleGenerateCopy(selectedTopicId)}
                  type="button"
                >
                  {busyKey === `generate-copy-${selectedTopicId}` ? '生成中...' : '生成文案'}
                </button>
              </div>

              <div className="copy-list">
                {copyVariants.length === 0 ? (
                  <EmptyState title="还没有文案" detail="为选中的选题生成文案后，这里会出现候选稿。" />
                ) : (
                  copyVariants.map((copy) => (
                    <article key={copy.id} className="copy-card">
                      <div className="list-card__meta">
                        <span>文案 #{copy.id}</span>
                        <span className={`pill pill--${copy.status}`}>{copy.status}</span>
                      </div>
                      <h4>{copy.title}</h4>
                      <p className="copy-card__hook">{copy.hook}</p>
                      <p className="copy-card__body">{copy.body}</p>
                      <div className="tag-row">
                        {copy.hashtags.map((tag) => (
                          <span key={tag} className="tag-chip">
                            {tag}
                          </span>
                        ))}
                      </div>
                      <label className="field">
                        <span className="field-label">创建审核任务备注</span>
                        <textarea
                          className="text-area text-area--compact"
                          rows={3}
                          value={notesByKey[`copy-${copy.id}`] ?? ''}
                          onChange={(event) =>
                            setNotesByKey((current) => ({
                              ...current,
                              [`copy-${copy.id}`]: event.target.value,
                            }))
                          }
                          placeholder="可选：补充审核关注点"
                        />
                      </label>
                      <button
                        className="button button--primary"
                        disabled={busyKey === `create-review-${copy.id}`}
                        onClick={() => handleCreateReviewTask(copy.id)}
                        type="button"
                      >
                        {busyKey === `create-review-${copy.id}` ? '创建中...' : '送审'}
                      </button>
                    </article>
                  ))
                )}
              </div>
            </section>
          </div>
        </section>

        <aside className="panel stack-panel">
          <div className="panel-header">
            <div>
              <p className="section-kicker">审核台</p>
              <h2>任务队列</h2>
            </div>
            <button className="button button--ghost" onClick={loadReviewTasks} type="button">
              刷新
            </button>
          </div>

          <div className="stack-list">
            {reviewTasks.length === 0 ? (
              <EmptyState title="审核队列为空" detail="先从中间区域选择一条文案送审。" />
            ) : (
              reviewTasks.map((task) => (
                <article key={task.id} className="review-card">
                  <div className="list-card__meta">
                    <span>任务 #{task.id}</span>
                    <span className={`pill pill--${task.review_status}`}>{task.review_status}</span>
                  </div>
                  <p>
                    热点 #{task.hotspot_id}
                    {task.topic_candidate_id ? ` / 选题 #${task.topic_candidate_id}` : ''}
                    {task.copy_variant_id ? ` / 文案 #${task.copy_variant_id}` : ''}
                  </p>
                  <label className="field">
                    <span className="field-label">审核备注</span>
                    <textarea
                      className="text-area text-area--compact"
                      rows={3}
                      value={notesByKey[`task-${task.id}`] ?? task.review_notes ?? ''}
                      onChange={(event) =>
                        setNotesByKey((current) => ({
                          ...current,
                          [`task-${task.id}`]: event.target.value,
                        }))
                      }
                      placeholder="记录通过或驳回原因"
                    />
                  </label>
                  <div className="decision-row">
                    <button
                      className="button button--success"
                      disabled={busyKey === `approve-${task.id}` || task.review_status === 'approved'}
                      onClick={() => handleReviewDecision(task.id, 'approve')}
                      type="button"
                    >
                      {busyKey === `approve-${task.id}` ? '处理中...' : '通过'}
                    </button>
                    <button
                      className="button button--danger"
                      disabled={busyKey === `reject-${task.id}` || task.review_status === 'rejected'}
                      onClick={() => handleReviewDecision(task.id, 'reject')}
                      type="button"
                    >
                      {busyKey === `reject-${task.id}` ? '处理中...' : '驳回'}
                    </button>
                  </div>
                </article>
              ))
            )}
          </div>
        </aside>
      </section>
    </main>
  )
}
