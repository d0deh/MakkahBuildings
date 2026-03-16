"""Core pipeline: generate_report() function.

This is the main entry point for report generation, designed to be
called by both the CLI and a future desktop GUI.
"""
from __future__ import annotations
import sys
from io import BytesIO
from pathlib import Path
from datetime import datetime

from .data.loader import load_excel
from .data.aggregator import aggregate
from .data.models import AreaStatistics, SurveyRecord
from .charts.bar_charts import (
    chart_building_presence, chart_building_type, chart_building_condition,
    chart_construction_method, chart_exterior_finish, chart_floor_distribution,
    chart_building_usage, chart_road_type, chart_road_width,
)
from .charts.pie_charts import chart_occupancy, chart_lighting, chart_parking
from .charts.map_chart import chart_map
from .presentation.report_builder import build_report
from .config import OUTPUT_DIR


def _safe_print(msg: str):
    """Print that won't crash on Windows with Arabic text."""
    try:
        print(msg)
    except (UnicodeEncodeError, UnicodeDecodeError):
        try:
            print(msg.encode('utf-8', errors='replace').decode('ascii', errors='replace'))
        except Exception:
            pass


def generate_report(
    excel_path: str,
    output_dir: str | None = None,
    use_ai: bool = True,
    template_path: str | None = None,
    on_progress: callable = None,
) -> str:
    """Generate a full PowerPoint report from survey Excel data.

    This is the clean, decoupled function that the future desktop app will call.

    Args:
        excel_path: Path to the survey .xlsx file
        output_dir: Directory for output file (default: project output/)
        use_ai: If True, use Claude API for analysis; if False, generate without AI
        template_path: Optional base .pptx template
        on_progress: Optional callback(step: str, pct: int) for progress updates

    Returns:
        Path to the generated .pptx file
    """
    def progress(step: str, pct: int):
        if on_progress:
            on_progress(step, pct)
        _safe_print(f"  [{pct:3d}%] {step}")

    # === Step 1: Load data ===
    progress("تحميل البيانات...", 5)
    records, warnings = load_excel(excel_path)
    if warnings:
        for w in warnings:
            _safe_print(f"  ⚠ {w}")

    # === Step 2: Aggregate statistics ===
    progress("حساب الإحصائيات...", 10)
    stats = aggregate(records)

    # === Step 3: Generate charts ===
    progress("إنشاء الرسوم البيانية...", 15)
    charts = _generate_all_charts(stats, records)
    progress(f"تم إنشاء {len(charts)} رسم بياني", 40)

    # === Step 4: AI analysis (if enabled) ===
    ai_content: dict[str, str | None] = {}
    if use_ai:
        progress("تحليل البيانات بالذكاء الاصطناعي...", 45)
        ai_content = _generate_ai_content(stats)
        progress("اكتمل التحليل الذكي", 75)
    else:
        progress("تم تخطي التحليل الذكي (--no-ai)", 75)

    # === Step 5: Build PowerPoint ===
    progress("تجميع التقرير...", 80)
    if output_dir is None:
        output_dir = str(OUTPUT_DIR)

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Output filename from area name and timestamp
    area_clean = stats.area_name.replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"تقرير_{area_clean}_{timestamp}.pptx"

    result = build_report(stats, charts, ai_content, output_path, template_path)
    progress(f"تم حفظ التقرير: {result}", 100)

    return result


def _generate_all_charts(stats: AreaStatistics, records: list[SurveyRecord]) -> dict[str, BytesIO]:
    """Generate all chart images."""
    charts = {}

    charts["presence"] = chart_building_presence(stats)
    charts["building_type"] = chart_building_type(stats)
    charts["building_condition"] = chart_building_condition(stats)
    charts["construction"] = chart_construction_method(stats)
    charts["finish"] = chart_exterior_finish(stats)
    charts["floors"] = chart_floor_distribution(stats)
    charts["building_usage"] = chart_building_usage(stats)
    charts["occupancy"] = chart_occupancy(stats)
    charts["road_type"] = chart_road_type(stats)
    charts["road_width"] = chart_road_width(stats)
    charts["lighting"] = chart_lighting(stats)
    charts["parking"] = chart_parking(stats)

    try:
        charts["map"] = chart_map(records)
    except Exception as e:
        _safe_print(f"  ⚠ Map generation failed: {e}")

    return charts


def _generate_ai_content(stats: AreaStatistics) -> dict[str, str | None]:
    """Generate all AI content via the 4-stage pipeline."""
    from .ai.analyst import analyze_data
    from .ai.describer import describe_chart, describe_infrastructure, describe_occupancy
    from .ai.insights import generate_insights
    from .ai.recommender import generate_recommendations

    content: dict[str, str | None] = {}

    # Stage 1: Full analysis
    try:
        _safe_print("    Stage 1: تحليل شامل للبيانات...")
        content["analysis"] = analyze_data(stats)
    except Exception as e:
        _safe_print(f"    ⚠ Analysis failed: {e}")
        content["analysis"] = None

    # Stage 2: Per-chart descriptions
    chart_descriptions = [
        ("desc_presence", "وجود المباني", {
            "يوجد مبنى": stats.total_with_buildings,
            "لا يوجد مبنى": stats.total_without_buildings,
        }),
        ("desc_building_type", "أنواع المباني", stats.building_types),
        ("desc_building_condition", "حالة المباني", stats.building_conditions),
        ("desc_construction", "أساليب الإنشاء", stats.construction_methods),
        ("desc_finish", "حالة التشطيب الخارجي", stats.exterior_finishes),
        ("desc_floors", "توزيع الطوابق", stats.floor_distribution),
        ("desc_building_usage", "استخدامات المباني", stats.building_usages),
    ]

    for key, title, data in chart_descriptions:
        try:
            _safe_print(f"    Stage 2: وصف {title}...")
            content[key] = describe_chart(title, data, stats.area_name)
        except Exception as e:
            _safe_print(f"    ⚠ Description failed for {title}: {e}")
            content[key] = None

    # Occupancy description
    try:
        _safe_print("    Stage 2: وصف الإشغال...")
        content["desc_occupancy"] = describe_occupancy(
            stats.total_residential_occupied, stats.total_residential_vacant,
            stats.total_commercial_occupied, stats.total_commercial_vacant,
            stats.area_name,
        )
    except Exception as e:
        _safe_print(f"    ⚠ Occupancy description failed: {e}")
        content["desc_occupancy"] = None

    # Infrastructure description
    try:
        _safe_print("    Stage 2: وصف البنية التحتية...")
        content["desc_infrastructure"] = describe_infrastructure(
            stats.road_types,
            stats.road_lighting_yes, stats.road_lighting_no,
            stats.parking_yes, stats.parking_no,
            stats.area_name,
        )
    except Exception as e:
        _safe_print(f"    ⚠ Infrastructure description failed: {e}")
        content["desc_infrastructure"] = None

    # Stage 3: Cross-data insights
    try:
        _safe_print("    Stage 3: استخراج العلاقات...")
        content["insights"] = generate_insights(stats)
    except Exception as e:
        _safe_print(f"    ⚠ Insights failed: {e}")
        content["insights"] = None

    # Stage 4: Recommendations
    try:
        _safe_print("    Stage 4: التوصيات...")
        content["recommendations"] = generate_recommendations(stats)
    except Exception as e:
        _safe_print(f"    ⚠ Recommendations failed: {e}")
        content["recommendations"] = None

    return content
