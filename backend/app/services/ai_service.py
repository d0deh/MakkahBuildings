"""AI analysis service — wraps the 4-stage pipeline."""
from __future__ import annotations
from ..core.models import AreaStatistics
from ..ai.analyst import analyze_data
from ..ai.describer import describe_chart, describe_infrastructure, describe_occupancy
from ..ai.insights import generate_insights
from ..ai.recommender import generate_recommendations

AI_SECTIONS = [
    "analysis", "desc_presence", "desc_building_type", "desc_building_condition",
    "desc_construction", "desc_finish", "desc_floors", "desc_building_usage",
    "desc_occupancy", "desc_infrastructure",
    "desc_road_type", "desc_road_width", "desc_lighting", "desc_parking", "desc_compliance",
    "insights", "recommendations",
]

def generate_ai_section(section: str, stats: AreaStatistics, use_cache: bool = True) -> str | None:
    """Generate a single AI section."""
    try:
        if section == "analysis":
            return analyze_data(stats)
        elif section == "insights":
            return generate_insights(stats)
        elif section == "recommendations":
            return generate_recommendations(stats)
        elif section == "desc_occupancy":
            return describe_occupancy(
                stats.total_residential_occupied, stats.total_residential_vacant,
                stats.total_commercial_occupied, stats.total_commercial_vacant,
                stats.area_name,
            )
        elif section == "desc_infrastructure":
            return describe_infrastructure(
                stats.road_types,
                stats.road_lighting_yes, stats.road_lighting_no,
                stats.parking_yes, stats.parking_no,
                stats.area_name,
            )
        elif section == "desc_road_type":
            return describe_chart("أنواع الطرق", stats.road_types, stats.area_name)
        elif section == "desc_road_width":
            return describe_chart("توزيع عرض الطرق", stats.road_width_distribution, stats.area_name)
        elif section == "desc_lighting":
            return describe_chart("إنارة الطرق", {"توجد": stats.road_lighting_yes, "لا توجد": stats.road_lighting_no}, stats.area_name)
        elif section == "desc_parking":
            return describe_chart("توفر المواقف", {"توجد": stats.parking_yes, "لا توجد": stats.parking_no}, stats.area_name)
        elif section == "desc_compliance":
            return describe_chart("حالة الامتثال", {"ممتثل": stats.compliant_count, "غير ممتثل": stats.non_compliant_count, "غير محدد": stats.na_compliance_count}, stats.area_name)
        elif section.startswith("desc_"):
            chart_data_map = {
                "desc_presence": ("وجود المباني", {"يوجد مبنى": stats.total_with_buildings, "لا يوجد مبنى": stats.total_without_buildings}),
                "desc_building_type": ("أنواع المباني", stats.building_types),
                "desc_building_condition": ("حالة المباني", stats.building_conditions),
                "desc_construction": ("أساليب الإنشاء", stats.construction_methods),
                "desc_finish": ("حالة التشطيب الخارجي", stats.exterior_finishes),
                "desc_floors": ("توزيع الطوابق", stats.floor_distribution),
                "desc_building_usage": ("استخدامات المباني", stats.building_usages),
            }
            if section in chart_data_map:
                title, data = chart_data_map[section]
                return describe_chart(title, data, stats.area_name)
        return None
    except Exception as e:
        print(f"AI section {section} failed: {e}")
        return None

def generate_all_ai(stats: AreaStatistics) -> dict[str, str | None]:
    content = {}
    for section in AI_SECTIONS:
        content[section] = generate_ai_section(section, stats)
    return content
