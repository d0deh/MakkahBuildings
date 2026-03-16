"""Regenerate endpoint — re-run a single AI section."""
from __future__ import annotations
import asyncio
from fastapi import APIRouter, HTTPException
from ..services.session import get_session
from ..services.ai_service import generate_ai_section, AI_SECTIONS

router = APIRouter(prefix="/api/sessions/{session_id}", tags=["regenerate"])

@router.post("/ai/{section}/regenerate")
async def regenerate_section(session_id: str, section: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    if section not in AI_SECTIONS:
        raise HTTPException(400, f"قسم غير معروف: {section}")

    text = await asyncio.to_thread(generate_ai_section, section, session.stats, use_cache=False)
    session.ai_content[section] = text

    return {"section": section, "text": text}
