# Plantaah - Eco-Farming Context Analyzer

A geospatial analytics platform that helps ecological farmers and landscape architects perform rapid site analysis by automating topography, climate, and vegetation data collection. Users draw a property boundary on an interactive map and receive a personalized 12-month eco-farming guide via email.

## Architecture

- **Frontend**: Vue.js 3 + Vite + Leaflet.js (port 5000 in dev)
- **Backend**: Python FastAPI + ReportLab (port 8000 in dev)
- **Map Library**: Leaflet.js loaded from CDN with leaflet-draw for polygon drawing

## Development

- Frontend dev server: `cd frontend && npm run dev` (port 5000)
- Backend dev server: `python -m uvicorn backend.main:app --host localhost --port 8000 --reload`
- Frontend proxies `/api/*` requests to `http://localhost:8000`

## Production

Uses `start.sh` which builds the Vue frontend into `frontend/dist/`, then serves everything via FastAPI (which also serves static files).

## Key Files

- `frontend/` — Vue.js 3 SPA
  - `src/views/AnalyzerView.vue` — Main submission form + map
  - `src/views/AdminView.vue` — Admin dashboard
  - `src/components/MapComponent.vue` — Leaflet polygon drawing
- `backend/main.py` — FastAPI app with all endpoints
- `start.sh` — Production startup script

## API Endpoints

- `POST /submit-analysis` — Submit site for analysis
- `GET /health` — Health check
- `GET /admin/submissions` — List submissions (admin)
- `GET /admin/export` — Export CSV (admin)

## User Preferences

- Keep the eco/nature green color scheme
- South African context (Cape Town default map center) but globally applicable
