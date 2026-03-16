"""Stage 1: Full data analysis — key findings, patterns, anomalies."""
from __future__ import annotations
from ..core.models import AreaStatistics
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
    user_prompt = f"""قدم ملخصاً تنفيذياً من 5 نقاط رئيسية فقط لمنطقة {stats.area_name}.

الشكل المطلوب:
• [رقم رئيسي] — [ملاحظة] — [لماذا هذا مهم]
• [رقم رئيسي] — [ملاحظة] — [لماذا هذا مهم]
• [رقم رئيسي] — [ملاحظة] — [لماذا هذا مهم]
• [رقم رئيسي] — [ملاحظة] — [لماذا هذا مهم]
• [رقم رئيسي] — [ملاحظة] — [لماذا هذا مهم]

البيانات:
{format_stats_for_ai(stats)}"""

    result = ask_claude(SYSTEM_ANALYST, user_prompt)

    # Post-process: ensure exactly 5 bullets
    lines = result.strip().split("\n")
    bullets = [l for l in lines if l.strip().startswith("•")]
    if len(bullets) > 5:
        bullets = bullets[:5]
        result = "\n".join(bullets)

    return result
