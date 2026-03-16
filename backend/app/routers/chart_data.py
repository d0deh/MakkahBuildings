"""Chart data endpoint — returns structured JSON for frontend Recharts."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException
from ..services.session import get_session
from ..services.chart_data_service import build_chart_data

router = APIRouter(prefix="/api/sessions/{session_id}", tags=["chart_data"])


@router.get("/chart-data")
async def get_chart_data(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")
    return build_chart_data(session.stats)
