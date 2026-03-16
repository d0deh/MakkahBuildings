"""PPTX export service — generates PowerPoint reports from session data."""
from __future__ import annotations
import base64
import threading
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches

from ..services.session import SessionData
from ..services.chart_service import generate_chart, CHART_TITLES
from ..presentation.slide_builders import (
    build_title_slide,
    build_summary_slide,
    build_chart_slide,
    build_map_slide,
    build_narrative_slide,
)

_mpl_lock = threading.Lock()

# Chart ordering for slides
CHART_ORDER = [
    "presence",
    "building_type",
    "building_condition",
    "construction",
    "finish",
    "floors",
    "building_usage",
    "occupancy",
    "road_type",
    "road_width",
    "lighting",
    "parking",
]

# Map section names to slide titles
SECTION_TITLES = {
    "analysis": "الملخص التنفيذي",
    "insights": "رؤى متقاطعة من البيانات",
    "recommendations": "التوصيات",
}


def _base64_to_bytesio(data_url: str) -> BytesIO:
    """Convert a data URL base64 string to BytesIO."""
    if data_url.startswith("data:"):
        data_url = data_url.split(",", 1)[1]
    buf = BytesIO(base64.b64decode(data_url))
    buf.seek(0)
    return buf


def generate_pptx(
    session: SessionData,
    sections: list[str] | None = None,
    edited_texts: dict[str, str] | None = None,
    pinned_items: list[dict] | None = None,
) -> BytesIO:
    """Generate a PPTX report from session data.

    Args:
        session: The session data containing stats, charts, and AI content
        sections: List of section IDs to include (None = all)
        edited_texts: Map of section_id -> edited text to override AI content
        pinned_items: List of pinned chat items to add as extra slides
    """
    edited_texts = edited_texts or {}
    pinned_items = pinned_items or []
    stats = session.stats

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Date range
    date_range = "غير محدد"
    if stats.date_min and stats.date_max:
        date_range = f"{stats.date_min[:10]} — {stats.date_max[:10]}"

    # 1. Title slide (always included)
    build_title_slide(prs, stats.area_name, stats.total_records, date_range)

    # 2. Executive summary
    if sections is None or "analysis" in sections:
        analysis_text = edited_texts.get("analysis", session.ai_content.get("analysis"))
        build_summary_slide(prs, stats, analysis_text)

    # 3. Chart slides
    for chart_name in CHART_ORDER:
        if sections is not None and chart_name not in sections:
            continue

        # Get chart image
        chart_b64 = session.charts.get(chart_name)
        if not chart_b64:
            try:
                with _mpl_lock:
                    chart_b64 = generate_chart(chart_name, stats, session.records)
                session.charts[chart_name] = chart_b64
            except Exception:
                continue

        chart_buf = _base64_to_bytesio(chart_b64)
        title = CHART_TITLES.get(chart_name, chart_name)

        # Get description (edited or original)
        desc_key = f"desc_{chart_name}"
        description = edited_texts.get(desc_key, session.ai_content.get(desc_key))

        if chart_name == "map":
            build_map_slide(prs, chart_buf)
        else:
            build_chart_slide(prs, title, chart_buf, description)

    # 4. Map slide
    if sections is None or "map" in sections:
        map_b64 = session.charts.get("map")
        if map_b64:
            map_buf = _base64_to_bytesio(map_b64)
            build_map_slide(prs, map_buf)

    # 5. Insights
    if sections is None or "insights" in sections:
        insights_text = edited_texts.get("insights", session.ai_content.get("insights"))
        if insights_text:
            build_narrative_slide(prs, "رؤى متقاطعة من البيانات", insights_text)

    # 6. Recommendations
    if sections is None or "recommendations" in sections:
        rec_text = edited_texts.get("recommendations", session.ai_content.get("recommendations"))
        if rec_text:
            build_narrative_slide(prs, "التوصيات", rec_text)

    # 7. Pinned items as extra slides
    for item in pinned_items:
        text = item.get("text", "")
        if text:
            build_narrative_slide(prs, "رؤى إضافية", text)

    # Save to BytesIO
    output = BytesIO()
    prs.save(output)
    output.seek(0)
    return output
