"""Slide dimensions, positions, fonts, and color definitions for PPTX."""
from __future__ import annotations
from pptx.util import Inches
from pptx.dml.color import RGBColor

# Slide dimensions (widescreen 16:9)
SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Colors as RGBColor
CLR_NAVY = RGBColor(0x1B, 0x2A, 0x4A)
CLR_GOLD = RGBColor(0xC9, 0xA8, 0x4C)
CLR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CLR_LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
CLR_DARK_GRAY = RGBColor(0x33, 0x33, 0x33)

# Font name for PPTX
PPTX_FONT = "Cairo"

# Common positions
TITLE_LEFT = Inches(0.5)
TITLE_TOP = Inches(0.3)
TITLE_WIDTH = Inches(12.333)
TITLE_HEIGHT = Inches(0.8)

# Chart slide positions
CHART_LEFT = Inches(0.5)
CHART_TOP = Inches(1.3)
CHART_WIDTH = Inches(7.5)
CHART_HEIGHT = Inches(5.5)

DESC_LEFT = Inches(8.3)
DESC_TOP = Inches(1.3)
DESC_WIDTH = Inches(4.5)
DESC_HEIGHT = Inches(5.5)

# Full-width chart (for map)
FULL_CHART_LEFT = Inches(0.5)
FULL_CHART_TOP = Inches(1.3)
FULL_CHART_WIDTH = Inches(12.333)
FULL_CHART_HEIGHT = Inches(5.5)

# Stat card dimensions
CARD_WIDTH = Inches(2.8)
CARD_HEIGHT = Inches(2.0)
CARD_SPACING = Inches(0.3)
