"""Global configuration — adapted from src/config.py for FastAPI backend."""
from __future__ import annotations
import os
from pathlib import Path
from pydantic_settings import BaseSettings


# Paths
BACKEND_ROOT = Path(__file__).parent.parent
FONTS_DIR = BACKEND_ROOT / "fonts"
UPLOAD_DIR = BACKEND_ROOT / "uploads"
CACHE_DIR = BACKEND_ROOT / ".ai_cache"

# Colors (Dark palette)
NAVY = "#1B2A4A"
GOLD = "#C9A84C"
LIGHT_NAVY = "#2D4A7A"
DARK_GOLD = "#A68A3E"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#F5F5F5"
DARK_GRAY = "#333333"

# Condition colors (dark-mode friendly)
COLOR_GOOD = "#2EA043"
COLOR_MODERATE = "#D29922"
COLOR_BAD = "#DA3633"
COLOR_NEUTRAL = "#78909C"

# Chart color sequence (muted blue as default instead of navy)
CHART_COLORS = ["#3B82AA", GOLD, "#4A90D9", "#E67E22", "#27AE60", "#8E44AD", "#C0392B", "#16A085"]

# Font (Noto Sans Arabic has full Arabic presentation forms needed by arabic_reshaper)
FONT_NAME = "Noto Sans Arabic"
FONT_FILE = "NotoSansArabic-Regular.ttf"
FONT_FALLBACK = "Sakkal Majalla"

# AI
AI_MODEL = "claude-sonnet-4-20250514"
AI_MAX_TOKENS = 2000

# "لا ينطبق" — the N/A value in Arabic
NA_VALUE = "لا ينطبق"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    ANTHROPIC_API_KEY: str = ""
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    UPLOAD_DIR: str = str(UPLOAD_DIR)

    model_config = {"env_file": str(BACKEND_ROOT / ".env"), "extra": "ignore"}


settings = Settings()
