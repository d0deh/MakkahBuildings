"""Data cleaning: typo normalization, NA handling, type coercion."""
from __future__ import annotations
import re
from ..config import NA_VALUE

# Column J (site_usage) typo normalization → all variants map to "مبنى مزال"
_SITE_USAGE_NORMALIZED = "مبنى مزال"
_SITE_USAGE_TYPOS = re.compile(
    r"^(مينى\s*مزال|مبنى\s*مرال|مبنى\.\s*مزال|ميني\s*مزال|"
    r"مبى\s*مزال|ملنى\s*مزال|مبني\s*مزال|مبنى\s+مزال)$"
)

# Shorten long building type labels for chart readability
_BUILDING_TYPE_SHORT = {
    "عمارة (عدة وحدات  في مبنى واحد )": "عمارة",
    "عمارة (عدة وحدات في مبنى واحد )": "عمارة",
    "بيت شعبي (وحدة سكنية واحدة بدون حوش وبدون باب للحوش)": "بيت شعبي",
    "هنجر-صندقة-شنكو": "هنجر/شنكو",
}

# Shorten construction method labels
_CONSTRUCTION_SHORT = {
    "هيكل خرساني (خرسانة مسلحة)": "هيكل خرساني",
    "حوائط حاملة (بدون أعمدة خرسانية)": "حوائط حاملة",
    "مباني خشبية أو معدنية": "خشبية/معدنية",
}

# Shorten finish labels
_FINISH_SHORT = {
    "ممتاز (تشطيب حديث، ديلوكس، سوبرديلوكس)": "ممتاز",
    "جيد جدًا (حالة متوسطة بتشطيب غير حديث)": "جيد جدًا",
    "جيد (تشطيب غير حديث وبه عيوب)": "جيد",
    "سيء (به الكثير من العيوب)": "سيء",
}

# Shorten building condition labels
_CONDITION_SHORT = {
    "مبنى مكتمل الإنشاء": "مكتمل",
}


def clean_string(value) -> str:
    """Strip whitespace, normalize None/empty to ''."""
    if value is None:
        return ""
    return str(value).strip()


def clean_optional_int(value) -> int | None:
    """Parse int from value, treating NA_VALUE and non-numeric as None."""
    if value is None:
        return None
    s = str(value).strip()
    if s == NA_VALUE or s == "" or s == "None":
        return None
    try:
        return int(float(s))
    except (ValueError, TypeError):
        return None


def clean_optional_float(value) -> float | None:
    """Parse float from value."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def normalize_site_usage(value: str) -> str:
    """Normalize column J typos to standard 'مبنى مزال'."""
    v = value.strip()
    if v == NA_VALUE or v == "":
        return v
    if _SITE_USAGE_TYPOS.match(v) or v == _SITE_USAGE_NORMALIZED:
        return _SITE_USAGE_NORMALIZED
    return v


def shorten_building_type(value: str) -> str:
    """Shorten building type label for charts."""
    return _BUILDING_TYPE_SHORT.get(value, value)


def shorten_construction(value: str) -> str:
    """Shorten construction method label for charts."""
    return _CONSTRUCTION_SHORT.get(value, value)


def shorten_finish(value: str) -> str:
    """Shorten finish label for charts."""
    return _FINISH_SHORT.get(value, value)


def shorten_condition(value: str) -> str:
    """Shorten building condition label for charts."""
    return _CONDITION_SHORT.get(value, value)


def is_na(value: str) -> bool:
    """Check if value is the Arabic N/A marker."""
    return value.strip() == NA_VALUE or value.strip() == ""
