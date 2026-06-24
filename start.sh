#!/bin/bash
# Build frontend for production
cd frontend && npm run build && cd ..

# Serve both: FastAPI serves the Vue build as static files + API
python -m uvicorn backend.main:app --host 0.0.0.0 --port 5000
