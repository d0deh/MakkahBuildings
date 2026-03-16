"""Conversational chat with survey data context."""
from __future__ import annotations
from ..core.models import AreaStatistics, SurveyRecord
from ..services.query_service import query_data
from .client import ask_claude
from .prompts import SYSTEM_CHAT, format_stats_for_ai


def chat_with_data(
    stats: AreaStatistics,
    message: str,
    history: list[dict],
    records: list[SurveyRecord] | None = None,
) -> str:
    """Chat with Claude using full area statistics as context.

    If records are provided, attempts a pandas query pipeline first
    for precise data answers.
    """
    # Try query pipeline for precise answers
    query_result_text = ""
    if records:
        result = query_data(records, message)
        if result:
            query_result_text = (
                f"نتيجة الاستعلام المحسوب من البيانات الخام:\n"
                f"الاستعلام: {result['query']}\n"
                f"النتيجة: {result['result']}"
            )

    system = SYSTEM_CHAT.format(
        stats_text=format_stats_for_ai(stats),
        query_result=query_result_text,
    )

    # Build conversation for Claude — flatten history + new message
    messages_text = ""
    for msg in history[-10:]:  # Keep last 10 messages for context
        role = "المستخدم" if msg.get("role") == "user" else "المحلل"
        messages_text += f"\n{role}: {msg['content']}"

    user_prompt = f"""المحادثة السابقة:{messages_text}

السؤال الجديد: {message}"""

    return ask_claude(system, user_prompt, use_cache=False)
