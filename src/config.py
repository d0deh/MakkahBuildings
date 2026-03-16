"""Global configuration constants."""
import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
FONTS_DIR = PROJECT_ROOT / "fonts"
OUTPUT_DIR = PROJECT_ROOT / "output"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CACHE_DIR = PROJECT_ROOT / ".ai_cache"

# Colors (Navy + Gold palette)
NAVY = "#1B2A4A"
GOLD = "#C9A84C"
LIGHT_NAVY = "#2D4A7A"
DARK_GOLD = "#A68A3E"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"
DARK_GRAY = "#333333"

# Condition colors
COLOR_GOOD = "#2E7D32"       # Green
COLOR_MODERATE = "#F9A825"   # Amber
COLOR_BAD = "#C62828"        # Red
COLOR_NEUTRAL = "#78909C"    # Blue-gray

# Chart color sequence
CHART_COLORS = [NAVY, GOLD, "#4A90D9", "#E67E22", "#27AE60", "#8E44AD", "#C0392B", "#16A085"]

# Font (Noto Sans Arabic has full Arabic presentation forms needed by arabic_reshaper)
FONT_NAME = "Noto Sans Arabic"
FONT_FILE = "NotoSansArabic-Regular.ttf"
FONT_FALLBACK = "Sakkal Majalla"

# AI
AI_MODEL = "claude-sonnet-4-20250514"
AI_MAX_TOKENS = 2000

# Slide dimensions (widescreen 16:9)
SLIDE_WIDTH_EMU = 12192000   # 13.333 inches
SLIDE_HEIGHT_EMU = 6858000   # 7.5 inches

# "لا ينطبق" — the N/A value in Arabic
NA_VALUE = "لا ينطبق"
