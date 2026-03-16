"""File upload endpoint."""
from __future__ import annotations
import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..core.loader import load_excel
from ..core.aggregator import aggregate
from ..services.session import create_session

router = APIRouter(prefix="/api", tags=["upload"])

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(400, "يرجى رفع ملف Excel (.xlsx)")

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        records, warnings = load_excel(tmp_path)
        stats = aggregate(records)
        session_id = create_session(records, stats, warnings=warnings)

        return {
            "session_id": session_id,
            "validation": {
                "total_rows": stats.total_records,
                "rows_with_buildings": stats.total_with_buildings,
                "empty_plots": stats.total_without_buildings,
                "date_range": {"start": stats.date_min, "end": stats.date_max},
                "area_name": stats.area_name,
                "warnings": warnings,
            },
        }
    except Exception as e:
        raise HTTPException(500, f"فشل في قراءة الملف: {str(e)}")
    finally:
        Path(tmp_path).unlink(missing_ok=True)
