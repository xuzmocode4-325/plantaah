#!/bin/bash
# Build frontend for production only — uvicorn is started separately by the run command
cd frontend && npm run build
