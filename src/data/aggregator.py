"""Aggregate survey records into AreaStatistics."""
from __future__ import annotations
from collections import Counter
from .models import SurveyRecord, AreaStatistics
from .cleaner import (
    is_na, shorten_building_type, shorten_construction,
    shorten_finish, shorten_condition,
)
from ..config import NA_VALUE


def aggregate(records: list[SurveyRecord]) -> AreaStatistics:
    """Compute all statistics from a list of survey records."""
    if not records:
        raise ValueError("No records to aggregate")

    area_name = records[0].area

    # Building presence
    has_yes = sum(1 for r in records if r.has_building == "نعم")
    has_no = sum(1 for r in records if r.has_building == "لا")
    has_linked = sum(1 for r in records if r.has_building == "تابع لعنوان وطني آخر")

    # Site type (for plots without buildings)
    site_types = Counter(
        r.site_type for r in records
        if not is_na(r.site_type)
    )

    # Site usage (with normalized typos)
    site_usages = Counter(
        r.site_usage for r in records
        if not is_na(r.site_usage)
    )

    # Building-level stats (only where has_building == "نعم")
    buildings = [r for r in records if r.has_building == "نعم"]

    building_types = Counter(
        shorten_building_type(r.building_type) for r in buildings
        if not is_na(r.building_type)
    )

    building_conditions = Counter(
        shorten_condition(r.building_condition) for r in buildings
        if not is_na(r.building_condition)
    )

    construction_methods = Counter(
        shorten_construction(r.construction_method) for r in buildings
        if not is_na(r.construction_method)
    )

    exterior_finishes = Counter(
        shorten_finish(r.exterior_finish) for r in buildings
        if not is_na(r.exterior_finish)
    )

    floor_distribution = Counter(
        r.floor_count for r in buildings
        if r.floor_count is not None
    )
    # Convert keys to str for JSON serialization
    floor_distribution = {str(k): v for k, v in sorted(floor_distribution.items())}

    building_usages = Counter(
        r.building_usage.strip() for r in buildings
        if not is_na(r.building_usage)
    )

    # Occupancy totals
    res_occ = sum(r.residential_occupied or 0 for r in buildings if r.residential_occupied is not None)
    res_vac = sum(r.residential_vacant or 0 for r in buildings if r.residential_vacant is not None)
    com_occ = sum(r.commercial_occupied or 0 for r in buildings if r.commercial_occupied is not None)
    com_vac = sum(r.commercial_vacant or 0 for r in buildings if r.commercial_vacant is not None)
    svc = sum(r.service_units or 0 for r in buildings if r.service_units is not None)

    # Road infrastructure (all records)
    road_types = Counter(r.road_type for r in records if not is_na(r.road_type))

    road_widths = Counter(
        int(r.road_width) for r in records
        if r.road_width is not None
    )
    road_width_dist = {str(k): v for k, v in sorted(road_widths.items())}

    light_yes = sum(1 for r in records if r.road_lighting == "نعم")
    light_no = sum(1 for r in records if r.road_lighting == "لا")
    park_yes = sum(1 for r in records if r.has_parking == "نعم")
    park_no = sum(1 for r in records if r.has_parking == "لا")

    # Compliance
    compliant = sum(1 for r in records if r.compliance == "نعم")
    non_compliant = sum(1 for r in records if r.compliance == "لا")
    na_compliance = sum(1 for r in records if is_na(r.compliance) or r.compliance == NA_VALUE)
    non_comp_reasons = [
        r.non_compliance_reason for r in records
        if not is_na(r.non_compliance_reason)
    ]

    # GPS bounds
    lats = [r.latitude for r in records if r.latitude is not None]
    lngs = [r.longitude for r in records if r.longitude is not None]

    # Date range
    dates = [r.date for r in records if r.date]
    dates_sorted = sorted(dates) if dates else []

    return AreaStatistics(
        area_name=area_name,
        total_records=len(records),
        total_with_buildings=has_yes,
        total_without_buildings=has_no,
        total_linked_address=has_linked,
        site_types=dict(site_types),
        site_usages=dict(site_usages),
        building_types=dict(building_types),
        building_conditions=dict(building_conditions),
        construction_methods=dict(construction_methods),
        exterior_finishes=dict(exterior_finishes),
        floor_distribution=floor_distribution,
        building_usages=dict(building_usages),
        total_residential_occupied=res_occ,
        total_residential_vacant=res_vac,
        total_commercial_occupied=com_occ,
        total_commercial_vacant=com_vac,
        total_service_units=svc,
        road_types=dict(road_types),
        road_width_distribution=road_width_dist,
        road_lighting_yes=light_yes,
        road_lighting_no=light_no,
        parking_yes=park_yes,
        parking_no=park_no,
        compliant_count=compliant,
        non_compliant_count=non_compliant,
        na_compliance_count=na_compliance,
        non_compliance_reasons=non_comp_reasons,
        lat_min=min(lats) if lats else None,
        lat_max=max(lats) if lats else None,
        lng_min=min(lngs) if lngs else None,
        lng_max=max(lngs) if lngs else None,
        date_min=dates_sorted[0] if dates_sorted else None,
        date_max=dates_sorted[-1] if dates_sorted else None,
    )
