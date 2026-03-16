"""Bar and horizontal bar chart generators."""
from __future__ import annotations
from io import BytesIO
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from .arabic_text import ar, setup_arabic_font
from .theme import apply_theme, get_chart_colors, get_condition_color, get_finish_color, BG_COLOR, TEXT_COLOR, TEXT_MUTED
from ..config import NAVY, GOLD
from ..core.models import AreaStatistics


def _bar_chart(
    data: dict[str, int],
    title: str,
    xlabel: str = "",
    ylabel: str = "العدد",
    colors: list[str] | None = None,
    horizontal: bool = False,
    figsize: tuple = (10, 6),
    value_labels: bool = True,
) -> BytesIO:
    """Generic bar chart builder. Returns PNG as BytesIO."""
    setup_arabic_font()
    apply_theme()

    fig, ax = plt.subplots(figsize=figsize)

    labels = [ar(k) for k in data.keys()]
    values = list(data.values())

    if colors is None:
        colors = get_chart_colors(len(data))

    if horizontal:
        y_pos = np.arange(len(labels))
        bars = ax.barh(y_pos, values, color=colors, height=0.6, edgecolor='none')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlabel(ar(ylabel))
        if xlabel:
            ax.set_ylabel(ar(xlabel))
        ax.invert_yaxis()
        if value_labels:
            for bar, val in zip(bars, values):
                ax.text(bar.get_width() + max(values) * 0.02, bar.get_y() + bar.get_height() / 2,
                        str(val), ha='left', va='center', fontweight='bold', color=TEXT_COLOR, fontsize=10)
    else:
        x_pos = np.arange(len(labels))
        bars = ax.bar(x_pos, values, color=colors, width=0.6, edgecolor='none')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, rotation=0 if len(labels) <= 6 else 30, ha='center')
        ax.set_ylabel(ar(ylabel))
        if xlabel:
            ax.set_xlabel(ar(xlabel))
        if value_labels:
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.02,
                        str(val), ha='center', va='bottom', fontweight='bold', color=TEXT_COLOR, fontsize=10)

    ax.set_title(ar(title), fontsize=16, fontweight='bold', color=TEXT_COLOR, pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#21262D')
    ax.spines['left'].set_color('#21262D')
    ax.grid(axis='x' if horizontal else 'y', alpha=0.3)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_building_presence(stats: AreaStatistics) -> BytesIO:
    """Bar chart: buildings vs empty plots."""
    data = {}
    if stats.total_with_buildings > 0:
        data["يوجد مبنى"] = stats.total_with_buildings
    if stats.total_without_buildings > 0:
        data["لا يوجد مبنى"] = stats.total_without_buildings
    if stats.total_linked_address > 0:
        data["تابع لعنوان آخر"] = stats.total_linked_address

    return _bar_chart(
        data, "وجود المباني في العناوين الوطنية",
        colors=[GOLD, "#3B82AA", "#78909C"][:len(data)],
    )


def chart_building_type(stats: AreaStatistics) -> BytesIO:
    """Horizontal bar: building types."""
    data = dict(sorted(stats.building_types.items(), key=lambda x: -x[1]))
    return _bar_chart(data, "أنواع المباني", horizontal=True, figsize=(10, max(5, len(data) * 1.2)))


def chart_building_condition(stats: AreaStatistics) -> BytesIO:
    """Bar chart: building conditions with semantic colors."""
    data = dict(sorted(stats.building_conditions.items(), key=lambda x: -x[1]))
    colors = [get_condition_color(k) for k in data.keys()]
    return _bar_chart(data, "حالة المباني", colors=colors)


def chart_construction_method(stats: AreaStatistics) -> BytesIO:
    """Bar chart: construction methods."""
    data = dict(sorted(stats.construction_methods.items(), key=lambda x: -x[1]))
    return _bar_chart(data, "أساليب الإنشاء")


def chart_exterior_finish(stats: AreaStatistics) -> BytesIO:
    """Bar chart: exterior finish quality with semantic colors."""
    order = ["ممتاز", "جيد جدًا", "جيد", "سيء"]
    data = {}
    for k in order:
        if k in stats.exterior_finishes:
            data[k] = stats.exterior_finishes[k]
    for k, v in stats.exterior_finishes.items():
        if k not in data:
            data[k] = v

    colors = [get_finish_color(k) for k in data.keys()]
    return _bar_chart(data, "حالة التشطيب الخارجي", colors=colors)


def chart_floor_distribution(stats: AreaStatistics) -> BytesIO:
    """Bar chart: number of floors."""
    data = dict(sorted(stats.floor_distribution.items(), key=lambda x: int(x[0])))
    labeled = {f"{k} طابق": v for k, v in data.items()}
    return _bar_chart(labeled, "توزيع عدد الطوابق", xlabel="عدد الطوابق")


def chart_building_usage(stats: AreaStatistics) -> BytesIO:
    """Horizontal bar: building usage types."""
    data = dict(sorted(stats.building_usages.items(), key=lambda x: -x[1]))
    return _bar_chart(data, "استخدامات المباني", horizontal=True, figsize=(10, max(5, len(data) * 1.2)))


def chart_road_type(stats: AreaStatistics) -> BytesIO:
    """Bar chart: road types."""
    data = dict(sorted(stats.road_types.items(), key=lambda x: -x[1]))
    return _bar_chart(data, "أنواع الطرق")


def chart_road_width(stats: AreaStatistics) -> BytesIO:
    """Bar chart: road width distribution."""
    data = dict(sorted(stats.road_width_distribution.items(), key=lambda x: int(x[0])))
    labeled = {f"{k}م": v for k, v in data.items()}
    return _bar_chart(labeled, "توزيع عرض الطرق (متر)", xlabel="العرض (م)")
