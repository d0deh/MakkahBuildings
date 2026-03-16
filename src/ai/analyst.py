"""Stage 1: Full data analysis — key findings, patterns, anomalies."""
from __future__ import annotations
from ..data.models import AreaStatistics
from .client import ask_claude
from .prompts import SYSTEM_ANALYST, format_stats_for_ai


def analyze_data(stats: AreaStatistics) -> str:
    """Send full statistics to Claude for comprehensive analysis.

    Returns Arabic analysis text covering:
    - Key findings
    - Notable patterns
    - Anomalies or red flags
    - Cross-column correlations
    """
    user_prompt = f"""حلل البيانات التالية لمنطقة {stats.area_name} وقدم:
1. أبرز النتائج الرئيسية (3-4 نقاط)
2. الأنماط الملفتة في البيانات
3. أي مؤشرات تحتاج اهتمام فوري
4. علاقات مهمة بين المتغيرات

البيانات:
{format_stats_for_ai(stats)}"""

    return ask_claude(SYSTEM_ANALYST, user_prompt)
