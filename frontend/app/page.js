const cards = [
  {
    title: '学习区',
    description: '沉淀技术架构、学习路线和能力地图。',
    items: ['技术架构图', '12 周学习路线', '学习与项目映射'],
  },
  {
    title: '工作区',
    description: '沉淀项目设计、接口设计、表结构和执行拆解。',
    items: ['系统架构', '数据库草案', 'API 草案', '分阶段实施'],
  },
]

export default function HomePage() {
  return (
    <main className="page-shell">
      <section className="hero">
        <p className="eyebrow">XHS AI Content Workflow</p>
        <h1>AI 图文内容工厂 V1 骨架</h1>
        <p className="lead">
          当前版本先服务于一个目标：把热点录入、文案生成、图片生成、人工审核这条链路稳定跑通。
        </p>
      </section>

      <section className="grid">
        {cards.map((card) => (
          <article key={card.title} className="card">
            <h2>{card.title}</h2>
            <p>{card.description}</p>
            <ul>
              {card.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </article>
        ))}
      </section>

      <section className="next-steps">
        <h2>下一步开发顺序</h2>
        <ol>
          <li>后端补充热点录入、选题生成、文案生成接口</li>
          <li>前端补充审核列表和详情页</li>
          <li>接入真实 LLM 和图片生成能力</li>
          <li>接入采集器和异步任务</li>
        </ol>
      </section>
    </main>
  )
}
