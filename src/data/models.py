"""Pydantic models for survey records and aggregated statistics."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class SurveyRecord(BaseModel):
    """A single row from the urban survey Excel file."""
    survey_id: str                          # A: رقم الاستبانة
    area: str                               # B: المنطقة
    supervisor: str                         # C: المشرف
    date: Optional[str] = None              # D: التاريخ
    national_address: Optional[str] = None  # E: العنوان الوطني
    longitude: Optional[float] = None       # F: الطول
    latitude: Optional[float] = None        # G: العرض
    has_building: str = ""                   # H: هل هناك مباني
    site_type: str = ""                     # I: نوع الموقع
    site_usage: str = ""                    # J: استخدام الموقع
    sub_address: str = ""                   # K: العنوان التابع
    building_count: Optional[int] = None    # L: عدد المباني
    building_type: str = ""                 # M: نوع المبنى
    building_condition: str = ""            # N: حالة المبنى
    construction_method: str = ""           # O: أسلوب الانشاء
    exterior_finish: str = ""               # P: حالة التشطيب الخارجي
    floor_count: Optional[int] = None       # Q: عدد الطوابق
    building_usage: str = ""                # R: استخدام المبنى
    residential_occupied: Optional[int] = None   # S: الوحدات السكنية المشغولة
    residential_vacant: Optional[int] = None     # T: الوحدات السكنية الخالية
    commercial_occupied: Optional[int] = None    # U: الوحدات التجارية المشغولة
    commercial_vacant: Optional[int] = None      # V: الوحدات التجارية الخالية
    service_units: Optional[int] = None          # W: الوحدات الخدمية
    service_type: str = ""                  # X: نوع استخدام المرفق الخدمي
    shelter_type: str = ""                  # Y: نوع مبنى الايواء
    compliance: str = ""                    # Z: امتثال
    non_compliance_reason: str = ""         # AA: سبب عدم الامتثال
    mecca_identity: str = ""                # AB: الهوية المكية
    road_type: str = ""                     # AC: نوع الطريق
    road_width: Optional[float] = None      # AD: عرض الطريق
    road_lighting: str = ""                 # AE: انارة الطريق
    has_parking: str = ""                   # AF: مواقف
    notes: str = ""                         # AG: الملاحظات


class AreaStatistics(BaseModel):
    """Aggregated statistics for an entire survey area."""
    area_name: str
    total_records: int
    total_with_buildings: int
    total_without_buildings: int
    total_linked_address: int  # تابع لعنوان وطني آخر

    # Site type breakdown (for plots without buildings)
    site_types: dict[str, int] = {}
    # Site usage breakdown (مبنى مزال etc.)
    site_usages: dict[str, int] = {}

    # Building type breakdown
    building_types: dict[str, int] = {}
    # Building condition
    building_conditions: dict[str, int] = {}
    # Construction method
    construction_methods: dict[str, int] = {}
    # Exterior finish
    exterior_finishes: dict[str, int] = {}
    # Floor distribution
    floor_distribution: dict[str, int] = {}
    # Building usage
    building_usages: dict[str, int] = {}

    # Occupancy
    total_residential_occupied: int = 0
    total_residential_vacant: int = 0
    total_commercial_occupied: int = 0
    total_commercial_vacant: int = 0
    total_service_units: int = 0

    # Road infrastructure
    road_types: dict[str, int] = {}
    road_width_distribution: dict[str, int] = {}
    road_lighting_yes: int = 0
    road_lighting_no: int = 0
    parking_yes: int = 0
    parking_no: int = 0

    # Compliance
    compliant_count: int = 0
    non_compliant_count: int = 0
    na_compliance_count: int = 0
    non_compliance_reasons: list[str] = []

    # GPS bounds
    lat_min: Optional[float] = None
    lat_max: Optional[float] = None
    lng_min: Optional[float] = None
    lng_max: Optional[float] = None

    # Date range
    date_min: Optional[str] = None
    date_max: Optional[str] = None
