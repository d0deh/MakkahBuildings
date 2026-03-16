"""Chart theme: Dark palette matching frontend design."""
from __future__ import annotations
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from ..config import (
    NAVY, GOLD, LIGHT_NAVY, CHART_COLORS,
    COLOR_GOOD, COLOR_MODERATE, COLOR_BAD, COLOR_NEUTRAL,
)

# Dark theme colors
BG_COLOR = '#0D1117'
SURFACE_COLOR = '#161B22'
TEXT_COLOR = '#E6EDF3'
TEXT_MUTED = '#7D8590'
GRID_COLOR = '#21262D'


def apply_theme():
    """Apply dark chart theme to matplotlib."""
    plt.rcParams.update({
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': SURFACE_COLOR,
        'axes.edgecolor': GRID_COLOR,
        'axes.labelcolor': TEXT_MUTED,
        'axes.titleweight': 'bold',
        'axes.titlesize': 14,
        'axes.labelsize': 11,
        'xtick.color': TEXT_MUTED,
        'ytick.color': TEXT_MUTED,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'grid.color': GRID_COLOR,
        'grid.linewidth': 0.3,
        'figure.dpi': 200,
        'savefig.dpi': 200,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.2,
    })


def get_chart_colors(n: int) -> list[str]:
    """Get n colors from the chart palette, cycling if needed."""
    if n <= len(CHART_COLORS):
        return CHART_COLORS[:n]
    return [CHART_COLORS[i % len(CHART_COLORS)] for i in range(n)]


def get_condition_color(condition: str) -> str:
    """Get color based on building condition."""
    mapping = {
        'مكتمل': COLOR_GOOD,
        'مبنى مكتمل الإنشاء': COLOR_GOOD,
        'مهجور': COLOR_MODERATE,
        'متهدم': COLOR_BAD,
    }
    return mapping.get(condition, COLOR_NEUTRAL)


def get_finish_color(finish: str) -> str:
    """Get color based on finish quality."""
    mapping = {
        'ممتاز': '#1B5E20',
        'جيد جدًا': COLOR_GOOD,
        'جيد': COLOR_MODERATE,
        'سيء': COLOR_BAD,
    }
    return mapping.get(finish, COLOR_NEUTRAL)
