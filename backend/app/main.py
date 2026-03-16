"""FastAPI application entry point."""
from __future__ import annotations
import os
os.environ["PYTHONUTF8"] = "1"

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from .config import settings
from .routers import upload, analysis, regenerate, chart_data, chat, export

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title="Urban Survey Report API",
    description="مولد التقارير العمرانية",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(analysis.router)
app.include_router(regenerate.router)
app.include_router(chart_data.router)
app.include_router(chat.router)
app.include_router(export.router)

@app.get("/api/health")
async def health():
    return {"status": "ok", "api_key_set": bool(os.environ.get("ANTHROPIC_API_KEY"))}
