"""Pie and donut chart generators."""
from __future__ import annotations
from io import BytesIO
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from .arabic_text import ar, setup_arabic_font
from .theme import apply_theme, get_chart_colors
from ..config import NAVY, GOLD, COLOR_GOOD, COLOR_BAD, COLOR_MODERATE
from ..data.models import AreaStatistics


def _pie_chart(
    data: dict[str, int],
    title: str,
    colors: list[str] | None = None,
    donut: bool = False,
    figsize: tuple = (8, 8),
) -> BytesIO:
    """Generic pie/donut chart. Returns PNG as BytesIO."""
    setup_arabic_font()
    apply_theme()

    fig, ax = plt.subplots(figsize=figsize)

    labels = [ar(k) for k in data.keys()]
    values = list(data.values())
    total = sum(values)

    if colors is None:
        colors = get_chart_colors(len(data))

    def autopct_func(pct):
        count = int(round(pct * total / 100))
        return f'{count}\n({pct:.1f}%)'

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors,
        autopct=autopct_func,
        startangle=90, pctdistance=0.75 if donut else 0.6,
        textprops={'fontsize': 11, 'color': NAVY},
    )

    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight('bold')

    if donut:
        centre_circle = plt.Circle((0, 0), 0.50, fc='white')
        ax.add_patch(centre_circle)
        ax.text(0, 0, ar(f"المجموع\n{total}"), ha='center', va='center',
                fontsize=14, fontweight='bold', color=NAVY)

    ax.set_title(ar(title), fontsize=16, fontweight='bold', color=NAVY, pad=20)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor='white')
    plt.close(fig)
    buf.seek(0)
    return buf


def chart_occupancy(stats: AreaStatistics) -> BytesIO:
    """Donut chart: residential occupancy (occupied vs vacant)."""
    data = {}
    if stats.total_residential_occupied > 0:
        data["وحدات مشغولة"] = stats.total_residential_occupied
    if stats.total_residential_vacant > 0:
        data["وحدات خالية"] = stats.total_residential_vacant

    if not data:
        data["لا توجد بيانات"] = 1

    colors = [COLOR_GOOD, COLOR_BAD][:len(data)]
    return _pie_chart(data, "إشغال الوحدات السكنية", colors=colors, donut=True)


def chart_lighting(stats: AreaStatistics) -> BytesIO:
    """Pie chart: road lighting."""
    data = {}
    if stats.road_lighting_yes > 0:
        data["توجد إنارة"] = stats.road_lighting_yes
    if stats.road_lighting_no > 0:
        data["لا توجد إنارة"] = stats.road_lighting_no

    colors = [GOLD, NAVY][:len(data)]
    return _pie_chart(data, "إنارة الطرق")


def chart_parking(stats: AreaStatistics) -> BytesIO:
    """Pie chart: parking availability."""
    data = {}
    if stats.parking_yes > 0:
        data["توجد مواقف"] = stats.parking_yes
    if stats.parking_no > 0:
        data["لا توجد مواقف"] = stats.parking_no

    colors = [COLOR_GOOD, COLOR_MODERATE][:len(data)]
    return _pie_chart(data, "توفر المواقف")
