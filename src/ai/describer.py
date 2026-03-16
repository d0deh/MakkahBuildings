"""Stage 2: Per-slide chart descriptions (2-3 sentences each)."""
from __future__ import annotations
from .client import ask_claude
from .prompts import SYSTEM_DESCRIBER


def describe_chart(chart_title: str, chart_data: dict[str, int | float], area_name: str) -> str:
    """Generate a 2-3 sentence Arabic description for a specific chart.

    Args:
        chart_title: Arabic title of the chart
        chart_data: The data shown in the chart {label: value}
        area_name: Name of the surveyed area

    Returns:
        Arabic description paragraph
    """
    data_text = "\n".join(f"  {k}: {v}" for k, v in chart_data.items())
    total = sum(v for v in chart_data.values() if isinstance(v, (int, float)))

    user_prompt = f"""اكتب وصفاً موجزاً (2-3 جمل) للرسم البياني التالي:

عنوان الرسم: {chart_title}
المنطقة: {area_name}
المجموع: {total}
البيانات:
{data_text}"""

    return ask_claude(SYSTEM_DESCRIBER, user_prompt)


def describe_infrastructure(
    road_types: dict, lighting_yes: int, lighting_no: int,
    parking_yes: int, parking_no: int, area_name: str
) -> str:
    """Generate description for the road infrastructure slide."""
    data_text = "\n".join(f"  {k}: {v}" for k, v in road_types.items())

    user_prompt = f"""اكتب وصفاً موجزاً (2-3 جمل) لبيانات البنية التحتية:

المنطقة: {area_name}
أنواع الطرق:
{data_text}
إنارة الطرق: نعم={lighting_yes}, لا={lighting_no}
مواقف: نعم={parking_yes}, لا={parking_no}"""

    return ask_claude(SYSTEM_DESCRIBER, user_prompt)


def describe_occupancy(
    res_occupied: int, res_vacant: int,
    com_occupied: int, com_vacant: int,
    area_name: str
) -> str:
    """Generate description for the occupancy slide."""
    user_prompt = f"""اكتب وصفاً موجزاً (2-3 جمل) لبيانات الإشغال:

المنطقة: {area_name}
الوحدات السكنية المشغولة: {res_occupied}
الوحدات السكنية الخالية: {res_vacant}
الوحدات التجارية المشغولة: {com_occupied}
الوحدات التجارية الخالية: {com_vacant}"""

    return ask_claude(SYSTEM_DESCRIBER, user_prompt)
