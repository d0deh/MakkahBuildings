# Urban Survey Report Generator (مولد التقارير العمرانية)

## Architecture
- **Next.js 15 frontend** — Arabic RTL dashboard with Tailwind + shadcn/ui
- **FastAPI backend** — Python REST API serving data, charts (base64 PNG), and AI analysis
- **Session-based** — each upload creates an in-memory session with cached stats, charts, AI content
- Legacy Flask GUI and PPTX pipeline preserved in `src/` for reference

## Project Structure
```
frontend/     → Next.js 15 App Router (port 3000)
backend/      → FastAPI + uvicorn (port 8000)
src/          → Legacy CLI/Flask code (reference only)
sample_data/  → Test Excel files
```

## Tech Stack
### Frontend
- Next.js 15, TypeScript strict, Tailwind CSS, shadcn/ui
- Cairo font (Google Fonts), full RTL via `dir="rtl"`
- API proxy: Next.js rewrites `/api/*` → `http://localhost:8000/api/*`

### Backend
- FastAPI, uvicorn, pydantic v2, pydantic-settings
- matplotlib + arabic_reshaper + python-bidi for charts
- anthropic SDK for Claude API (4-stage AI analysis)
- Charts returned as base64 PNG data URLs

## Color Palette
- Navy: `#1B2A4A` (primary)
- Gold: `#C9A84C` (accent)
- Good: `#2E7D32`, Warning: `#F9A825`, Danger: `#C62828`

## Key Rules
- Every Arabic string in matplotlib MUST pass through `ar()` function
- `matplotlib.use('Agg')` before any imports
- API key from `os.environ["ANTHROPIC_API_KEY"]` — never hardcoded
- Dashboard must work without AI (show charts + stats, skip descriptions)
- All UI text is Arabic — no English in the interface
- Charts use thread lock (`_mpl_lock`) for matplotlib thread safety

## API Endpoints
```
POST /api/upload                              → Upload Excel, returns session_id + validation
GET  /api/sessions/{id}/stats                 → AreaStatistics JSON
GET  /api/sessions/{id}/charts                → All charts as base64
GET  /api/sessions/{id}/ai                    → All AI content
POST /api/sessions/{id}/ai/{section}/regenerate → Re-run one AI section
GET  /api/health                              → Health check
```

## Running
```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm run dev
```

## Data Schema
33-column Excel survey data from Mecca informal neighborhoods.
Key verification numbers (السرد dataset): 609 rows, 115 with buildings, 494 empty plots.

## AI Pipeline (4 stages)
1. **analyst.py** — Full data analysis (key findings, patterns, executive summary)
2. **describer.py** — Per-chart descriptions (2-3 Arabic sentences each)
3. **insights.py** — Cross-data correlations
4. **recommender.py** — Prioritized recommendations
