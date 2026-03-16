"""GPS scatter map chart over OSM basemap."""
from __future__ import annotations
from io import BytesIO
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from .arabic_text import ar, setup_arabic_font
from .theme import apply_theme, get_condition_color, BG_COLOR, TEXT_COLOR, TEXT_MUTED
from ..config import NAVY, GOLD, COLOR_GOOD, COLOR_BAD, COLOR_MODERATE, COLOR_NEUTRAL
from ..core.models import SurveyRecord


def chart_map(records: list[SurveyRecord], title: str = "خريطة مواقع المسح") -> BytesIO:
    """Generate a GPS scatter map colored by building presence.

    Tries contextily for OSM basemap, falls back to plain scatter.
    """
    setup_arabic_font()
    apply_theme()

    # Separate records by building presence
    # Note: In the Excel, col F (الطول) has lat values and col G (العرض) has lng values
    # The loader stores F→longitude and G→latitude, but the actual data is swapped
    has_building = [(r.longitude, r.latitude) for r in records
                    if r.has_building == "نعم" and r.longitude and r.latitude]
    no_building = [(r.longitude, r.latitude) for r in records
                   if r.has_building != "نعم" and r.longitude and r.latitude]

    fig, ax = plt.subplots(figsize=(12, 10))

    # Plot points
    if no_building:
        lats, lngs = zip(*no_building)
        ax.scatter(lngs, lats, c='#3B82AA', s=15, alpha=0.4, label=ar("بدون مبنى"), zorder=2)

    if has_building:
        lats, lngs = zip(*has_building)
        ax.scatter(lngs, lats, c=GOLD, s=40, alpha=0.8, label=ar("يوجد مبنى"),
                   edgecolors='#0D1117', linewidth=0.5, zorder=3)

    # Try to add OSM basemap
    try:
        import contextily as ctx
        import geopandas as gpd
        from shapely.geometry import Point

        all_points = has_building + no_building
        all_lats, all_lngs = zip(*all_points)

        # Create GeoDataFrame in EPSG:4326 then convert to Web Mercator
        gdf = gpd.GeoDataFrame(
            geometry=[Point(lng, lat) for lat, lng in all_points],
            crs="EPSG:4326"
        )
        gdf_web = gdf.to_crs(epsg=3857)

        # Re-plot in Web Mercator
        ax.clear()

        no_build_web = gdf_web.iloc[len(has_building):]
        has_build_web = gdf_web.iloc[:len(has_building)]

        if len(no_build_web) > 0:
            ax.scatter(
                no_build_web.geometry.x, no_build_web.geometry.y,
                c='#3B82AA', s=15, alpha=0.4, label=ar("بدون مبنى"), zorder=2
            )
        if len(has_build_web) > 0:
            ax.scatter(
                has_build_web.geometry.x, has_build_web.geometry.y,
                c=GOLD, s=40, alpha=0.8, label=ar("يوجد مبنى"),
                edgecolors='#0D1117', linewidth=0.5, zorder=3
            )

        try:
            ctx.add_basemap(ax, source=ctx.providers.CartoDB.DarkMatter, zoom=16)
        except Exception:
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=16)
        ax.set_axis_off()

    except Exception:
        # Fallback: plain scatter without basemap
        ax.set_xlabel(ar("خط الطول"), color=TEXT_MUTED)
        ax.set_ylabel(ar("خط العرض"), color=TEXT_MUTED)
        ax.grid(True, alpha=0.3)

    ax.set_title(ar(title), fontsize=16, fontweight='bold', color=TEXT_COLOR, pad=15)
    legend = ax.legend(loc='upper right', fontsize=11, framealpha=0.9,
                       facecolor='#161B22', edgecolor='#21262D', labelcolor=TEXT_COLOR)

    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    buf.seek(0)
    return buf
