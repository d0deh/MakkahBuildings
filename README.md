# مولد التقارير العمرانية — Urban Survey Report Generator

Web application for analyzing urban survey data from Mecca informal neighborhoods and generating AI-powered reports with charts and recommendations.

## Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- Anthropic API key (optional — app works without AI)

### Environment Variables

Copy `.env.example` to `.env` in the project root and/or `backend/.env`:

```
ANTHROPIC_API_KEY=your-key-here
CORS_ORIGINS=["http://localhost:3000"]
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## Usage

1. Upload an Excel file (.xlsx) with 33-column urban survey data
2. View statistics, charts, and AI-generated analysis on the dashboard
3. Regenerate any AI section individually if needed
