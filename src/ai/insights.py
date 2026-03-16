"""Stage 3: Cross-data correlations and insights."""
from __future__ import annotations
from ..data.models import AreaStatistics
from .client import ask_claude
from .prompts import SYSTEM_INSIGHTS, format_stats_for_ai


def generate_insights(stats: AreaStatistics) -> str:
    """Identify cross-variable correlations and patterns.

    Returns Arabic text with 4-6 insight paragraphs.
    """
    user_prompt = f"""بناءً على البيانات التالية، حدد العلاقات والارتباطات المهمة بين المتغيرات المختلفة:

{format_stats_for_ai(stats)}

ركز على:
- العلاقة بين حالة المباني وأسلوب الإنشاء
- العلاقة بين عرض الطرق وتوفر الإنارة والمواقف
- العلاقة بين نوع المباني واستخداماتها
- أي أنماط جغرافية أو هيكلية ملفتة"""

    return ask_claude(SYSTEM_INSIGHTS, user_prompt)
