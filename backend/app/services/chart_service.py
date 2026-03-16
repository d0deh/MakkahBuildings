"""Chart generation service — returns base64 PNG strings."""
from __future__ import annotations
import base64
import threading
from io import BytesIO
from ..core.models import AreaStatistics, SurveyRecord
from ..charts.bar_charts import (
    chart_building_presence, chart_building_type, chart_building_condition,
    chart_construction_method, chart_exterior_finish, chart_floor_distribution,
    chart_building_usage, chart_road_type, chart_road_width,
)
from ..charts.pie_charts import chart_occupancy, chart_lighting, chart_parking, chart_compliance
from ..charts.map_chart import chart_map

_mpl_lock = threading.Lock()

CHART_GENERATORS = {
    "presence": lambda stats, _, dpi=200: chart_building_presence(stats, dpi=dpi),
    "building_type": lambda stats, _, dpi=200: chart_building_type(stats, dpi=dpi),
    "building_condition": lambda stats, _, dpi=200: chart_building_condition(stats, dpi=dpi),
    "construction": lambda stats, _, dpi=200: chart_construction_method(stats, dpi=dpi),
    "finish": lambda stats, _, dpi=200: chart_exterior_finish(stats, dpi=dpi),
    "floors": lambda stats, _, dpi=200: chart_floor_distribution(stats, dpi=dpi),
    "building_usage": lambda stats, _, dpi=200: chart_building_usage(stats, dpi=dpi),
    "occupancy": lambda stats, _, dpi=200: chart_occupancy(stats, dpi=dpi),
    "road_type": lambda stats, _, dpi=200: chart_road_type(stats, dpi=dpi),
    "road_width": lambda stats, _, dpi=200: chart_road_width(stats, dpi=dpi),
    "lighting": lambda stats, _, dpi=200: chart_lighting(stats, dpi=dpi),
    "parking": lambda stats, _, dpi=200: chart_parking(stats, dpi=dpi),
    "compliance": lambda stats, _, dpi=200: chart_compliance(stats, dpi=dpi),
    "map": lambda _, records, dpi=200: chart_map(records, dpi=dpi),
}

CHART_TITLES = {
    "presence": "وجود المباني في العناوين الوطنية",
    "building_type": "أنواع المباني",
    "building_condition": "حالة المباني",
    "construction": "أساليب الإنشاء",
    "finish": "حالة التشطيب الخارجي",
    "floors": "توزيع عدد الطوابق",
    "building_usage": "استخدامات المباني",
    "occupancy": "إشغال الوحدات السكنية",
    "road_type": "نوع الطريق",
    "road_width": "عرض الطريق",
    "lighting": "إنارة الطريق",
    "parking": "مواقف السيارات",
    "compliance": "حالة الامتثال",
    "map": "خريطة مواقع المسح",
}

def _buf_to_base64(buf: BytesIO) -> str:
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode("ascii")

def generate_chart(chart_name: str, stats: AreaStatistics, records: list[SurveyRecord] | None = None, dpi: int = 200) -> str:
    gen = CHART_GENERATORS.get(chart_name)
    if not gen:
        raise ValueError(f"Unknown chart: {chart_name}")
    with _mpl_lock:
        buf = gen(stats, records, dpi=dpi)
    return _buf_to_base64(buf)

def generate_all_charts(stats: AreaStatistics, records: list[SurveyRecord]) -> dict[str, str]:
    charts = {}
    for name in CHART_GENERATORS:
        try:
            charts[name] = generate_chart(name, stats, records)
        except Exception as e:
            print(f"Chart {name} failed: {e}")
    return charts
