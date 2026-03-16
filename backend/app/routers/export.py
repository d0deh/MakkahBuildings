"""PPTX export endpoint."""
from __future__ import annotations
import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..services.session import get_session
from ..services.export_service import generate_pptx

router = APIRouter(prefix="/api/sessions/{session_id}", tags=["export"])


class ExportRequest(BaseModel):
    sections: list[str] | None = None
    edited_texts: dict[str, str] | None = None
    pinned_items: list[dict] | None = None


@router.post("/export")
async def export_pptx(session_id: str, req: ExportRequest):
    session = get_session(session_id)
    if not session:
        raise HTTPException(404, "الجلسة غير موجودة")

    try:
        output = await asyncio.to_thread(
            generate_pptx, session, req.sections, req.edited_texts, req.pinned_items
        )

        filename = f"report_{session.stats.area_name}_{session_id}.pptx"
        # RFC 5987: use filename* with UTF-8 encoding for non-ASCII filenames
        from urllib.parse import quote
        encoded = quote(filename)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded}"},
        )
    except Exception as e:
        raise HTTPException(500, f"خطأ في إنشاء التقرير: {str(e)}")
