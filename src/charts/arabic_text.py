"""Arabic text handling for matplotlib charts."""
from __future__ import annotations
import matplotlib
matplotlib.use('Agg')  # Must be before any other matplotlib imports

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
import arabic_reshaper
from bidi.algorithm import get_display

from ..config import FONTS_DIR, FONT_NAME, FONT_FILE, FONT_FALLBACK

_font_initialized = False
_font_path: str | None = None


def ar(text: str) -> str:
    """Reshape and reorder Arabic text for correct matplotlib rendering.

    Every Arabic string displayed in matplotlib MUST pass through this function.
    """
    if not text:
        return text
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)


def setup_arabic_font() -> str:
    """Register Arabic font with matplotlib. Returns the font family name to use."""
    global _font_initialized, _font_path

    if _font_initialized and _font_path:
        return FONT_NAME

    # Primary: bundled Noto Sans Arabic
    primary = FONTS_DIR / FONT_FILE
    if primary.exists():
        try:
            fm.fontManager.addfont(str(primary))
            prop = fm.FontProperties(fname=str(primary))
            font_family = prop.get_name()
            _font_path = str(primary)
            plt.rcParams['font.family'] = font_family
            plt.rcParams['font.sans-serif'] = [font_family, FONT_FALLBACK, 'Arial']
            _font_initialized = True
            return font_family
        except Exception:
            pass

    # Fallback to system Arabic fonts
    fallback_paths = [
        Path(f"C:/Windows/Fonts/{FONT_FALLBACK}.ttf"),
        Path("C:/Windows/Fonts/Tahoma.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for p in fallback_paths:
        if p.exists():
            try:
                fm.fontManager.addfont(str(p))
                prop = fm.FontProperties(fname=str(p))
                font_family = prop.get_name()
                _font_path = str(p)
                plt.rcParams['font.family'] = font_family
                _font_initialized = True
                return font_family
            except Exception:
                continue

    _font_initialized = True
    return 'sans-serif'


def get_font_path() -> str | None:
    """Return the resolved font file path."""
    if not _font_initialized:
        setup_arabic_font()
    return _font_path
