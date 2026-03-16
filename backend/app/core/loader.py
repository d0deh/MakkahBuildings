"""Load Excel survey data into SurveyRecord models."""
from __future__ import annotations
from pathlib import Path
import openpyxl
from .models import SurveyRecord
from .cleaner import (
    clean_string, clean_optional_int, clean_optional_float,
    normalize_site_usage,
)


def load_excel(file_path: str | Path) -> tuple[list[SurveyRecord], list[str]]:
    """Load survey Excel file and return (records, warnings).

    Args:
        file_path: Path to .xlsx file

    Returns:
        Tuple of (list of SurveyRecord, list of warning strings)
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Excel file not found: {path}")

    wb = openpyxl.load_workbook(str(path), read_only=True, data_only=True)
    ws = wb.active
    warnings: list[str] = []
    records: list[SurveyRecord] = []

    rows = list(ws.iter_rows(min_row=2, values_only=True))  # skip header

    for row_idx, row in enumerate(rows, start=2):
        if len(row) < 33:
            warnings.append(f"Row {row_idx}: only {len(row)} columns (expected 33)")
            # Pad with None
            row = tuple(list(row) + [None] * (33 - len(row)))

        # Parse date as string
        date_val = row[3]
        if date_val is not None:
            date_str = str(date_val)[:19]  # truncate to datetime
        else:
            date_str = None

        record = SurveyRecord(
            survey_id=clean_string(row[0]),
            area=clean_string(row[1]),
            supervisor=clean_string(row[2]),
            date=date_str,
            national_address=clean_string(row[4]) if row[4] is not None else None,
            longitude=clean_optional_float(row[5]),
            latitude=clean_optional_float(row[6]),
            has_building=clean_string(row[7]),
            site_type=clean_string(row[8]),
            site_usage=normalize_site_usage(clean_string(row[9])),
            sub_address=clean_string(row[10]),
            building_count=clean_optional_int(row[11]),
            building_type=clean_string(row[12]),
            building_condition=clean_string(row[13]),
            construction_method=clean_string(row[14]),
            exterior_finish=clean_string(row[15]),
            floor_count=clean_optional_int(row[16]),
            building_usage=clean_string(row[17]),
            residential_occupied=clean_optional_int(row[18]),
            residential_vacant=clean_optional_int(row[19]),
            commercial_occupied=clean_optional_int(row[20]),
            commercial_vacant=clean_optional_int(row[21]),
            service_units=clean_optional_int(row[22]),
            service_type=clean_string(row[23]),
            shelter_type=clean_string(row[24]),
            compliance=clean_string(row[25]),
            non_compliance_reason=clean_string(row[26]),
            mecca_identity=clean_string(row[27]),
            road_type=clean_string(row[28]),
            road_width=clean_optional_float(row[29]),
            road_lighting=clean_string(row[30]),
            has_parking=clean_string(row[31]),
            notes=clean_string(row[32]),
        )
        records.append(record)

    wb.close()
    return records, warnings
