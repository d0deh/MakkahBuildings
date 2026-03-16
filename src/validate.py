"""Standalone data validation and diagnostics script.

Usage: python -m src.validate "path/to/file.xlsx"
"""
from __future__ import annotations
import sys
from pathlib import Path
from collections import Counter


def validate_file(file_path: str) -> None:
    """Load an Excel file and print full diagnostics."""
    from .data.loader import load_excel
    from .data.aggregator import aggregate
    from .config import NA_VALUE

    path = Path(file_path)
    print(f"\n{'='*60}")
    print(f"  Data Validation: {path.name}")
    print(f"{'='*60}\n")

    records, warnings = load_excel(path)
    print(f"Total rows loaded: {len(records)}")

    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠ {w}")

    # Aggregate
    stats = aggregate(records)

    print(f"\nArea: {stats.area_name}")
    print(f"Date range: {stats.date_min} → {stats.date_max}")
    print(f"GPS: lat [{stats.lat_min:.6f}, {stats.lat_max:.6f}], lng [{stats.lng_min:.6f}, {stats.lng_max:.6f}]")

    print(f"\n--- Building Presence ---")
    print(f"  With buildings: {stats.total_with_buildings}")
    print(f"  Without buildings: {stats.total_without_buildings}")
    print(f"  Linked to other address: {stats.total_linked_address}")

    def print_dist(title: str, data: dict, sort_by_count: bool = True):
        print(f"\n--- {title} ---")
        items = sorted(data.items(), key=lambda x: -x[1]) if sort_by_count else sorted(data.items())
        for k, v in items:
            pct = v / len(records) * 100
            print(f"  [{v:5d}] ({pct:5.1f}%) {k}")

    print_dist("Site Type (no-building plots)", stats.site_types)
    print_dist("Site Usage", stats.site_usages)
    print_dist("Building Type", stats.building_types)
    print_dist("Building Condition", stats.building_conditions)
    print_dist("Construction Method", stats.construction_methods)
    print_dist("Exterior Finish", stats.exterior_finishes)
    print_dist("Floor Count", stats.floor_distribution, sort_by_count=False)
    print_dist("Building Usage", stats.building_usages)

    print(f"\n--- Occupancy ---")
    print(f"  Residential occupied units: {stats.total_residential_occupied}")
    print(f"  Residential vacant units: {stats.total_residential_vacant}")
    print(f"  Commercial occupied units: {stats.total_commercial_occupied}")
    print(f"  Commercial vacant units: {stats.total_commercial_vacant}")
    print(f"  Service units: {stats.total_service_units}")

    print_dist("Road Type", stats.road_types)
    print_dist("Road Width (m)", stats.road_width_distribution, sort_by_count=False)

    print(f"\n--- Infrastructure ---")
    print(f"  Lighting: Yes={stats.road_lighting_yes}, No={stats.road_lighting_no}")
    print(f"  Parking: Yes={stats.parking_yes}, No={stats.parking_no}")

    print(f"\n--- Compliance ---")
    print(f"  Compliant: {stats.compliant_count}")
    print(f"  Non-compliant: {stats.non_compliant_count}")
    print(f"  N/A: {stats.na_compliance_count}")
    if stats.non_compliance_reasons:
        print(f"  Reasons:")
        for r in stats.non_compliance_reasons:
            print(f"    - {r}")

    print(f"\n{'='*60}")
    print(f"  Validation complete. {len(records)} records processed.")
    print(f"{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.validate <excel_file>")
        sys.exit(1)
    validate_file(sys.argv[1])


if __name__ == "__main__":
    main()
