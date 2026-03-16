"""In-memory session store for uploaded data and computed results."""
from __future__ import annotations
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from ..core.models import SurveyRecord, AreaStatistics

@dataclass
class SessionData:
    session_id: str
    records: list[SurveyRecord]
    stats: AreaStatistics
    charts: dict[str, str] = field(default_factory=dict)  # chart_name -> base64
    ai_content: dict[str, str | None] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    chat_history: list[dict] = field(default_factory=list)
    pinned_items: list[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

_sessions: dict[str, SessionData] = {}
SESSION_TTL = timedelta(hours=2)

def create_session(records: list[SurveyRecord], stats: AreaStatistics, warnings: list[str] | None = None) -> str:
    session_id = uuid.uuid4().hex[:12]
    _sessions[session_id] = SessionData(
        session_id=session_id, records=records, stats=stats,
        warnings=warnings or [],
    )
    _cleanup_expired()
    return session_id

def get_session(session_id: str) -> SessionData | None:
    return _sessions.get(session_id)

def _cleanup_expired():
    now = datetime.now()
    expired = [k for k, v in _sessions.items() if now - v.created_at > SESSION_TTL]
    for k in expired:
        del _sessions[k]
