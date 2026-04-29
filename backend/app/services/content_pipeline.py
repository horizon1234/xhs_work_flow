from __future__ import annotations

from app.models.hotspot import Hotspot
from app.models.topic_candidate import TopicCandidate


def _compact_text(value: str, limit: int) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= limit:
        return normalized
    return f"{normalized[: limit - 1]}..."


def build_topic_candidates(hotspot: Hotspot) -> list[dict[str, object]]:
    keyword = hotspot.keyword.strip()
    title = hotspot.raw_title.strip()
    summary = hotspot.summary or _compact_text(hotspot.raw_content, 90)

    return [
        {
            "angle_type": "trend_summary",
            "title_hint": f"{keyword} 到底发生了什么？",
            "description": f"基于热点《{title}》快速解释来龙去脉，并提炼普通用户最需要知道的 3 个变化。",
            "audience": "想快速理解热点的人群",
            "relevance_score": 0.92,
            "risk_score": 0.18,
            "status": "topic_generated",
        },
        {
            "angle_type": "practical_advice",
            "title_hint": f"{keyword} 给普通人的 3 个提醒",
            "description": f"把热点内容转成可执行建议，重点围绕“{summary}”延展成经验型内容。",
            "audience": "希望获得方法论的人群",
            "relevance_score": 0.88,
            "risk_score": 0.22,
            "status": "topic_generated",
        },
        {
            "angle_type": "counter_intuition",
            "title_hint": f"别只盯着 {keyword}，真正值得注意的是这件事",
            "description": f"从反常识角度拆解《{title}》，给出一个更适合小红书表达的观点切口。",
            "audience": "更愿意看观点表达的人群",
            "relevance_score": 0.83,
            "risk_score": 0.28,
            "status": "topic_generated",
        },
    ]


def build_copy_variants(topic: TopicCandidate, hotspot: Hotspot) -> list[dict[str, object]]:
    keyword = hotspot.keyword.strip().replace(" ", "") or "热点"
    hashtags = [f"#{keyword}", "#小红书运营", "#内容创作"]

    return [
        {
            "model_name": "mock-llm",
            "prompt_version": "v1",
            "title": topic.title_hint,
            "hook": f"这条 {keyword} 热点，如果只看表面，你大概率会误判。",
            "body": (
                f"先说结论：{topic.description}\n\n"
                "如果你准备把这类话题写成小红书内容，最稳的结构是：先用一句话讲清事件，"
                "再提炼 3 个具体影响，最后补一段个人判断。这样既容易读完，也方便后续进入审核。"
            ),
            "hashtags": hashtags,
            "cover_text": _compact_text(topic.title_hint, 18),
            "comment_hint": "你会怎么判断这波热点后续走势？",
            "risk_notes": "当前为模拟生成结果，发布前需要补事实核验。",
            "status": "copy_generated",
        },
        {
            "model_name": "mock-llm",
            "prompt_version": "v1",
            "title": f"做 {keyword} 内容时，我更建议先想清楚这 1 点",
            "hook": f"很多人会直接追 {keyword}，但真正影响出稿质量的是切角。",
            "body": (
                f"这个选题更适合从“{topic.audience}”出发。\n\n"
                "正文建议先抛出现象，再讲为什么和普通人有关，最后给一个可以立刻执行的动作。"
                "这样更贴近平台阅读习惯，也更方便人工审核时快速判断可用性。"
            ),
            "hashtags": hashtags,
            "cover_text": _compact_text(f"{keyword} 内容切角", 18),
            "comment_hint": "如果你来写，会选解释型还是观点型？",
            "risk_notes": "建议补充来源链接和事实依据后再进入发布。",
            "status": "copy_generated",
        },
    ]