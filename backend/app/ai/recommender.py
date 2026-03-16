"""Stage 4: Prioritized recommendations."""
from __future__ import annotations
from ..core.models import AreaStatistics
from .client import ask_claude
from .prompts import SYSTEM_RECOMMENDER, format_stats_for_ai


def generate_recommendations(stats: AreaStatistics) -> str:
    """Generate 5-7 prioritized actionable recommendations.

    Returns numbered Arabic recommendations.
    """
    user_prompt = f"""بناءً على نتائج المسح العمراني التالية لمنطقة {stats.area_name}، قدم 5-7 توصيات مرتبة حسب الأولوية:

{format_stats_for_ai(stats)}

ضع في اعتبارك:
- نسبة المباني المزالة العالية ({stats.total_without_buildings} من {stats.total_records})
- حالة المباني المتبقية (المهجورة والمتهدمة)
- البنية التحتية (الطرق، الإنارة، المواقف)
- السلامة الإنشائية (أساليب البناء القديمة)
- جودة الحياة للسكان الحاليين"""

    return ask_claude(SYSTEM_RECOMMENDER, user_prompt)
