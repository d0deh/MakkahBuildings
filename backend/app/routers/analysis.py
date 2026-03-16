"""Analysis endpoints — stats, charts, AI content."""
from __future__ import annotations
import asyncio
from fastapi import APIRouter, HTTPException
from ..services.session import get_session
from ..services.chart_service import generate_all_charts, generate_chart, CHART_TITLES
from ..services.ai_service import generate_all_ai, generate_ai_section, AI_SECTIONS

router = APIRouter(prefix="/api/sessions/{session_id}", tags=["analysis"])

@router.get("/stats")
async def get_stats(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")
    return session.stats.model_dump()

@router.get("/charts")
async def get_charts(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    if not session.charts:
        charts = await asyncio.to_thread(generate_all_charts, session.stats, session.records)
        session.charts = charts

    return {
        "charts": [
            {"id": name, "title": CHART_TITLES.get(name, name), "image": img}
            for name, img in session.charts.items()
        ]
    }

@router.get("/charts/{chart_name}")
async def get_chart(session_id: str, chart_name: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    if chart_name not in session.charts:
        try:
            img = await asyncio.to_thread(generate_chart, chart_name, session.stats, session.records)
            session.charts[chart_name] = img
        except ValueError:
            raise HTTPException(400, f"رسم بياني غير معروف: {chart_name}")

    return {"id": chart_name, "title": CHART_TITLES.get(chart_name, chart_name), "image": session.charts[chart_name]}

@router.get("/ai")
async def get_ai_content(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    if not session.ai_content:
        content = await asyncio.to_thread(generate_all_ai, session.stats)
        session.ai_content = content

    return session.ai_content

@router.get("/validation")
async def get_validation(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")
    return {"warnings": session.warnings}

@router.get("/ai/{section}")
async def get_ai_section(session_id: str, section: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    if section not in AI_SECTIONS:
        raise HTTPException(400, f"قسم غير معروف: {section}")

    if section not in session.ai_content:
        text = await asyncio.to_thread(generate_ai_section, section, session.stats)
        session.ai_content[section] = text

    return {"section": section, "text": session.ai_content[section]}
