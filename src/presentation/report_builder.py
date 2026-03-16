"""Orchestrates full PPTX assembly from charts and AI content."""
from __future__ import annotations
from io import BytesIO
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Emu

from .styles import SLIDE_WIDTH, SLIDE_HEIGHT
from .slide_builders import (
    build_title_slide, build_summary_slide, build_chart_slide,
    build_map_slide, build_narrative_slide, build_road_infrastructure_slide,
)
from ..data.models import AreaStatistics


def build_report(
    stats: AreaStatistics,
    charts: dict[str, BytesIO],
    ai_content: dict[str, str | None],
    output_path: str | Path,
    template_path: str | Path | None = None,
) -> str:
    """Assemble the full PowerPoint report.

    Args:
        stats: Aggregated area statistics
        charts: Dict of chart name → PNG BytesIO buffer
        ai_content: Dict of AI-generated text content (can be None for --no-ai)
        output_path: Where to save the .pptx file
        template_path: Optional base template .pptx

    Returns:
        Path to the saved .pptx file
    """
    if template_path and Path(template_path).exists():
        prs = Presentation(str(template_path))
    else:
        prs = Presentation()

    # Set widescreen dimensions
    prs.slide_width = Emu(12192000)
    prs.slide_height = Emu(6858000)

    # Date range
    date_range = ""
    if stats.date_min and stats.date_max:
        date_range = f"{stats.date_min[:10]} — {stats.date_max[:10]}"

    # Helper to safely get AI content
    def ai(key: str) -> str | None:
        return ai_content.get(key)

    # Helper to reset BytesIO position
    def chart(name: str) -> BytesIO:
        buf = charts[name]
        buf.seek(0)
        return buf

    # === Slide 1: Title ===
    build_title_slide(prs, stats.area_name, stats.total_records, date_range)

    # === Slide 2: Executive Summary ===
    build_summary_slide(prs, stats, ai("analysis"))

    # === Slide 3: GPS Map ===
    if "map" in charts:
        build_map_slide(prs, chart("map"))

    # === Slide 4: Building Presence ===
    if "presence" in charts:
        build_chart_slide(prs, "وجود المباني في العناوين الوطنية",
                          chart("presence"), ai("desc_presence"))

    # === Slide 5: Building Types ===
    if "building_type" in charts:
        build_chart_slide(prs, "أنواع المباني",
                          chart("building_type"), ai("desc_building_type"))

    # === Slide 6: Building Condition ===
    if "building_condition" in charts:
        build_chart_slide(prs, "حالة المباني",
                          chart("building_condition"), ai("desc_building_condition"))

    # === Slide 7: Construction Method ===
    if "construction" in charts:
        build_chart_slide(prs, "أساليب الإنشاء",
                          chart("construction"), ai("desc_construction"))

    # === Slide 8: Exterior Finish ===
    if "finish" in charts:
        build_chart_slide(prs, "حالة التشطيب الخارجي",
                          chart("finish"), ai("desc_finish"))

    # === Slide 9: Floor Distribution ===
    if "floors" in charts:
        build_chart_slide(prs, "توزيع عدد الطوابق",
                          chart("floors"), ai("desc_floors"))

    # === Slide 10: Building Usage ===
    if "building_usage" in charts:
        build_chart_slide(prs, "استخدامات المباني",
                          chart("building_usage"), ai("desc_building_usage"))

    # === Slide 11: Occupancy ===
    if "occupancy" in charts:
        build_chart_slide(prs, "إشغال الوحدات السكنية",
                          chart("occupancy"), ai("desc_occupancy"))

    # === Slide 12: Road Infrastructure ===
    if all(k in charts for k in ["road_type", "road_width", "lighting", "parking"]):
        build_road_infrastructure_slide(
            prs,
            chart("road_type"), chart("road_width"),
            chart("lighting"), chart("parking"),
            ai("desc_infrastructure"),
        )

    # === Slide 13: Compliance ===
    compliance_text = _build_compliance_text(stats)
    if compliance_text:
        build_narrative_slide(prs, "الامتثال لاشتراطات المباني", compliance_text)

    # === Slide 14: Cross-Data Insights ===
    if ai("insights"):
        build_narrative_slide(prs, "رؤى وعلاقات مكتشفة من البيانات", ai("insights"))

    # === Slide 15: Recommendations ===
    if ai("recommendations"):
        build_narrative_slide(prs, "التوصيات", ai("recommendations"))

    # Save
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(output))
    return str(output)


def _build_compliance_text(stats: AreaStatistics) -> str:
    """Build compliance summary text."""
    total_checked = stats.compliant_count + stats.non_compliant_count
    lines = []
    lines.append(f"إجمالي المباني التي تم فحص امتثالها: {total_checked}")
    lines.append(f"ملتزمة: {stats.compliant_count}")
    lines.append(f"غير ملتزمة: {stats.non_compliant_count}")
    lines.append(f"لا ينطبق (عناوين بدون مباني): {stats.na_compliance_count}")

    if stats.non_compliance_reasons:
        lines.append("\nأسباب عدم الامتثال:")
        for reason in stats.non_compliance_reasons:
            items = [r.strip() for r in reason.split(",")]
            lines.append("• " + "، ".join(items))

    return "\n".join(lines)
