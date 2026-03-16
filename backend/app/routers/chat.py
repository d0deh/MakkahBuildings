"""Chat endpoints — conversational AI analysis."""
from __future__ import annotations
import uuid
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.session import get_session
from ..ai.chat import chat_with_data

router = APIRouter(prefix="/api/sessions/{session_id}", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


class PinRequest(BaseModel):
    message_id: str
    text: str
    chart_spec: dict | None = None


@router.post("/chat")
async def chat(session_id: str, req: ChatRequest):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    try:
        reply = await asyncio.to_thread(
            chat_with_data, session.stats, req.message, req.history, session.records
        )
        message_id = uuid.uuid4().hex[:8]

        # Store in session history
        if not hasattr(session, "chat_history"):
            session.chat_history = []
        session.chat_history.append({"role": "user", "content": req.message})
        session.chat_history.append({"role": "assistant", "content": reply})

        return {"reply": reply, "message_id": message_id}
    except EnvironmentError:
        raise HTTPException(503, "مفتاح API غير مُعد. يرجى تعيين ANTHROPIC_API_KEY")
    except Exception as e:
        raise HTTPException(500, f"خطأ في المحادثة: {str(e)}")


@router.post("/pin")
async def pin_item(session_id: str, req: PinRequest):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    if not hasattr(session, "pinned_items"):
        session.pinned_items = []

    session.pinned_items.append({
        "message_id": req.message_id,
        "text": req.text,
        "chart_spec": req.chart_spec,
    })
    return {"ok": True}


@router.delete("/pin/{message_id}")
async def unpin_item(session_id: str, message_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    if hasattr(session, "pinned_items"):
        session.pinned_items = [
            p for p in session.pinned_items if p["message_id"] != message_id
        ]
    return {"ok": True}


@router.get("/pins")
async def get_pins(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    items = getattr(session, "pinned_items", [])
    return {"items": items}
