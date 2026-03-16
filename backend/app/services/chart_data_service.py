"""Chart data service — returns structured JSON for frontend Recharts."""
from __future__ import annotations
from ..core.models import AreaStatistics


def build_chart_data(stats: AreaStatistics) -> dict:
    """Map each chart ID to {type, title, data: [{name, value}]}."""
    charts = {}

    # Presence
    charts["presence"] = {
        "type": "bar",
        "title": "وجود المباني في العناوين الوطنية",
        "data": [
            {"name": "يوجد مبنى", "value": stats.total_with_buildings},
            {"name": "لا يوجد مبنى", "value": stats.total_without_buildings},
        ],
    }

    # Building type
    charts["building_type"] = {
        "type": "bar",
        "title": "أنواع المباني",
        "data": [{"name": k, "value": v} for k, v in stats.building_types.items()],
    }

    # Building condition
    charts["building_condition"] = {
        "type": "bar",
        "title": "حالة المباني",
        "data": [{"name": k, "value": v} for k, v in stats.building_conditions.items()],
        "colorMap": {
            "ممتاز": "#2EA043",
            "مكتمل": "#2EA043",
            "جيد جدًا": "#3B82AA",
            "جيد": "#D29922",
            "سيء": "#DA3633",
            "مهجور": "#DA3633",
            "تحت الإنشاء": "#546E7A",
        },
    }

    # Construction
    charts["construction"] = {
        "type": "bar",
        "title": "أساليب الإنشاء",
        "data": [{"name": k, "value": v} for k, v in stats.construction_methods.items()],
    }

    # Finish
    charts["finish"] = {
        "type": "bar",
        "title": "حالة التشطيب الخارجي",
        "data": [{"name": k, "value": v} for k, v in stats.exterior_finishes.items()],
        "colorMap": {
            "ممتاز": "#2EA043",
            "جيد جدًا": "#3B82AA",
            "جيد": "#D29922",
            "سيء": "#DA3633",
        },
    }

    # Floors
    charts["floors"] = {
        "type": "bar",
        "title": "توزيع عدد الطوابق",
        "data": [
            {"name": f"{k} طابق", "value": v}
            for k, v in sorted(stats.floor_distribution.items(), key=lambda x: int(x[0]))
        ],
    }

    # Building usage
    charts["building_usage"] = {
        "type": "bar",
        "title": "استخدامات المباني",
        "data": [{"name": k, "value": v} for k, v in stats.building_usages.items()],
    }

    # Occupancy — pie
    charts["occupancy"] = {
        "type": "pie",
        "title": "إشغال الوحدات السكنية",
        "data": [
            {"name": "سكنية مشغولة", "value": stats.total_residential_occupied},
            {"name": "سكنية خالية", "value": stats.total_residential_vacant},
            {"name": "تجارية مشغولة", "value": stats.total_commercial_occupied},
            {"name": "تجارية خالية", "value": stats.total_commercial_vacant},
        ],
    }

    # Road type
    charts["road_type"] = {
        "type": "bar",
        "title": "نوع الطريق",
        "data": [{"name": k, "value": v} for k, v in stats.road_types.items()],
    }

    # Road width
    charts["road_width"] = {
        "type": "bar",
        "title": "عرض الطريق",
        "data": [
            {"name": f"{k}م", "value": v}
            for k, v in sorted(stats.road_width_distribution.items(), key=lambda x: int(x[0]))
        ],
    }

    # Lighting — pie
    charts["lighting"] = {
        "type": "pie",
        "title": "إنارة الطريق",
        "data": [
            {"name": "توجد إنارة", "value": stats.road_lighting_yes},
            {"name": "لا توجد إنارة", "value": stats.road_lighting_no},
        ],
    }

    # Parking — pie
    charts["parking"] = {
        "type": "pie",
        "title": "مواقف السيارات",
        "data": [
            {"name": "توجد مواقف", "value": stats.parking_yes},
            {"name": "لا توجد مواقف", "value": stats.parking_no},
        ],
    }

    # Map stays as backend image
    charts["map"] = None

    return charts
