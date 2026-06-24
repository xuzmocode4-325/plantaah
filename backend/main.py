import asyncio
import json
import uuid
import logging
import csv
import io
import os
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, field_validator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plantaah API",
    description="Eco-Farming Context Analyzer API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SubmissionStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class PolygonModel(BaseModel):
    type: str = "Polygon"
    coordinates: list


class SubmissionRequest(BaseModel):
    project_name: str
    email: EmailStr
    polygon: PolygonModel
    area_hectares: float

    @field_validator("project_name")
    @classmethod
    def validate_project_name(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Project name must be at least 3 characters")
        return v.strip()

    @field_validator("area_hectares")
    @classmethod
    def validate_area(cls, v):
        if v < 0.1 or v > 500:
            raise ValueError("Area must be between 0.1 and 500 hectares")
        return v


class Submission(BaseModel):
    id: str
    project_name: str
    email: str
    polygon: dict
    area_hectares: float
    status: SubmissionStatus
    analysis_data: Optional[dict] = None
    pdf_url: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None
    error_message: Optional[str] = None


# In-memory store (replace with real DB in production)
submissions_db: dict[str, dict] = {}


async def fetch_topography(polygon_coords: list) -> dict:
    """Fetch elevation/topography data from OpenTopography API (simulated with graceful fallback)."""
    try:
        # Calculate bounding box
        lons = [c[0] for c in polygon_coords[0] if c]
        lats = [c[1] for c in polygon_coords[0] if c]
        south, north = min(lats), max(lats)
        west, east = min(lons), max(lons)

        # Try OpenTopography API (free, no key needed for SRTM)
        url = "https://portal.opentopography.org/API/globaldem"
        params = {
            "demtype": "SRTMGL3",
            "south": south, "north": north,
            "west": west, "east": east,
            "outputFormat": "JSON",
            "API_Key": "demoapikeyot2022"
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "elevation_min": data.get("minElevation", 50),
                    "elevation_max": data.get("maxElevation", 300),
                    "slope_class": "Moderate (5-15%)",
                    "source": "OpenTopography SRTM"
                }
    except Exception as e:
        logger.warning(f"OpenTopography API call failed: {e}, using estimated values")

    # Fallback: estimated values based on South Africa averages
    return {
        "elevation_min": 45,
        "elevation_max": 280,
        "slope_class": "Gentle to Moderate (2-12%)",
        "source": "Estimated (API unavailable)"
    }


async def fetch_climate(polygon_coords: list) -> dict:
    """Fetch climate data (simulated with representative Cape Town / ZA data)."""
    await asyncio.sleep(0.5)  # Simulate API call
    return {
        "temperature_min_c": 8,
        "temperature_max_c": 32,
        "annual_rainfall_mm": 520,
        "drought_risk": "Moderate",
        "wind_direction": "South-Southeast (Cape Doctor)",
        "frost_risk": "Low (coastal zone)",
        "growing_days": 280,
        "source": "Climate Engine (estimated)"
    }


async def fetch_vegetation(polygon_coords: list) -> dict:
    """Fetch NDVI / vegetation data (simulated)."""
    await asyncio.sleep(0.5)
    return {
        "ndvi_score": 0.42,
        "vegetation_cover_pct": 38,
        "bare_land_pct": 62,
        "vegetation_type": "Fynbos / Mixed Shrub",
        "source": "Sentinel Hub (estimated)"
    }


async def fetch_with_retry(coro, max_retries=3, delay=5):
    """Retry a coroutine up to max_retries times with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return await coro
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"Attempt {attempt+1} failed: {e}, retrying in {delay}s")
            await asyncio.sleep(delay)


def generate_crop_recommendations(climate: dict, vegetation: dict, topography: dict) -> list:
    """Generate crop recommendations based on analysis data."""
    rainfall = climate.get("annual_rainfall_mm", 500)
    frost_risk = climate.get("frost_risk", "Low")
    ndvi = vegetation.get("ndvi_score", 0.3)

    crops = []
    if rainfall >= 400:
        crops.extend([
            {"crop": "Rooibos Tea", "season": "Year-round", "suitability": "Excellent"},
            {"crop": "Protea", "season": "Spring/Summer", "suitability": "Excellent"},
        ])
    if rainfall >= 300:
        crops.extend([
            {"crop": "Olives", "season": "Autumn", "suitability": "Good"},
            {"crop": "Lavender", "season": "Spring/Summer", "suitability": "Good"},
        ])
    crops.extend([
        {"crop": "Indigenous Vegetables (Morogo)", "season": "Summer", "suitability": "Good"},
        {"crop": "Sunflowers", "season": "Spring/Summer", "suitability": "Moderate"},
        {"crop": "Sorghum", "season": "Summer", "suitability": "Moderate"},
    ])
    return crops


def generate_planting_calendar(climate: dict) -> list:
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    activities = [
        "Harvest summer crops, prepare beds",
        "Late summer harvest, start composting",
        "Autumn planting: garlic, onions, leafy greens",
        "Plant cool-season crops: spinach, kale, broccoli",
        "Protect tender plants, mulch beds",
        "Winter care: cover crops, soil amendment",
        "Mid-winter: plan spring beds, order seeds",
        "Early spring prep, start seedlings indoors",
        "Spring planting: tomatoes, peppers, beans",
        "Full planting season: all summer crops",
        "Summer crops growing, irrigation critical",
        "Harvest begins, preserve surplus"
    ]
    return [{"month": m, "activities": a} for m, a in zip(months, activities)]


async def generate_pdf_guide(submission: dict, analysis: dict) -> bytes:
    """Generate a PDF eco-farming guide using ReportLab."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm, cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    import io as _io

    buffer = _io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)

    styles = getSampleStyleSheet()
    GREEN = colors.HexColor('#2d6a4f')
    LIGHT_GREEN = colors.HexColor('#52b788')
    CREAM = colors.HexColor('#f8f4e3')

    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  textColor=GREEN, fontSize=24, spaceAfter=6)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
                               textColor=GREEN, fontSize=14, spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                 fontSize=10, leading=14, spaceAfter=6)
    center_style = ParagraphStyle('Center', parent=styles['Normal'],
                                   alignment=TA_CENTER, fontSize=10)

    story = []
    project_name = submission['project_name']
    email = submission['email']
    area = submission.get('area_hectares', 0)

    # Cover
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("🌱 Plantaah", title_style))
    story.append(Paragraph("Eco-Farming Context Analyzer", h2_style))
    story.append(HRFlowable(width="100%", color=LIGHT_GREEN, thickness=2))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"<b>12-Month Eco-Farming Guide</b>", styles['Heading1']))
    story.append(Paragraph(f"Project: {project_name}", body_style))
    story.append(Paragraph(f"Prepared for: {email}", body_style))
    story.append(Paragraph(f"Site Area: {area:.2f} hectares", body_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", body_style))
    story.append(Spacer(1, 1*cm))

    # Executive Summary
    crops = analysis.get('crop_recommendations', [])
    story.append(HRFlowable(width="100%", color=LIGHT_GREEN, thickness=1))
    story.append(Paragraph("Executive Summary", h2_style))
    top_crops = ', '.join([c['crop'] for c in crops[:3]]) if crops else "See crop guide below"
    story.append(Paragraph(f"<b>Top 3 Recommended Crops:</b> {top_crops}", body_style))
    story.append(Paragraph(
        f"<b>Water Strategy:</b> {analysis.get('climate', {}).get('drought_risk', 'N/A')} drought risk — "
        f"rainwater harvesting + drip irrigation recommended.", body_style))
    story.append(Paragraph(
        f"<b>Key Climate Risk:</b> {analysis.get('climate', {}).get('frost_risk', 'Low')} frost risk. "
        f"Monitor for summer drought periods.", body_style))

    # Site Overview
    topo = analysis.get('topography', {})
    story.append(Paragraph("Site Overview", h2_style))
    story.append(Table([
        ["Attribute", "Value"],
        ["Site Area", f"{area:.2f} hectares"],
        ["Elevation Range", f"{topo.get('elevation_min','N/A')}m – {topo.get('elevation_max','N/A')}m"],
        ["Slope Class", topo.get('slope_class', 'N/A')],
        ["Data Source", topo.get('source', 'N/A')],
    ], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
        ('PADDING', (0,0), (-1,-1), 6),
    ])))

    # Climate Profile
    climate = analysis.get('climate', {})
    story.append(Paragraph("Climate Profile", h2_style))
    story.append(Table([
        ["Metric", "Value"],
        ["Temperature Range", f"{climate.get('temperature_min_c','N/A')}°C – {climate.get('temperature_max_c','N/A')}°C"],
        ["Annual Rainfall", f"{climate.get('annual_rainfall_mm','N/A')} mm"],
        ["Drought Risk", climate.get('drought_risk', 'N/A')],
        ["Wind Direction", climate.get('wind_direction', 'N/A')],
        ["Frost Risk", climate.get('frost_risk', 'N/A')],
        ["Growing Days", f"{climate.get('growing_days','N/A')} days/year"],
    ], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
        ('PADDING', (0,0), (-1,-1), 6),
    ])))

    # Vegetation
    veg = analysis.get('vegetation', {})
    story.append(Paragraph("Vegetation Analysis", h2_style))
    story.append(Paragraph(f"<b>NDVI Score:</b> {veg.get('ndvi_score', 'N/A')} (0=bare, 1=dense vegetation)", body_style))
    story.append(Paragraph(f"<b>Vegetation Cover:</b> {veg.get('vegetation_cover_pct','N/A')}%", body_style))
    story.append(Paragraph(f"<b>Bare Land:</b> {veg.get('bare_land_pct','N/A')}%", body_style))
    story.append(Paragraph(f"<b>Vegetation Type:</b> {veg.get('vegetation_type','N/A')}", body_style))

    # Crop Recommendations
    story.append(Paragraph("Crop Recommendations", h2_style))
    if crops:
        crop_data = [["Crop", "Season", "Suitability"]]
        for c in crops:
            crop_data.append([c['crop'], c['season'], c['suitability']])
        story.append(Table(crop_data, style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), GREEN),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
            ('PADDING', (0,0), (-1,-1), 6),
        ])))

    # Planting Calendar
    calendar = analysis.get('planting_calendar', [])
    story.append(Paragraph("12-Month Planting Calendar", h2_style))
    if calendar:
        cal_data = [["Month", "Activities"]]
        for entry in calendar:
            cal_data.append([entry['month'], entry['activities']])
        story.append(Table(cal_data, colWidths=[3*cm, 14*cm], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), GREEN),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
            ('PADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ])))

    # Water Management
    story.append(Paragraph("Water Management Strategy", h2_style))
    story.append(Paragraph(
        f"Annual rainfall of {climate.get('annual_rainfall_mm','N/A')}mm suggests supplemental irrigation "
        f"is required during summer months (Nov–Feb). Recommended strategies:", body_style))
    for tip in [
        "Install rainwater harvesting tanks (minimum 5,000L per hectare)",
        "Use drip irrigation to reduce water loss by 30-50%",
        "Apply 5-8cm mulch layer around plants to retain moisture",
        "Plant windbreaks to reduce evapotranspiration",
        "Monitor soil moisture with tensiometers during drought periods"
    ]:
        story.append(Paragraph(f"• {tip}", body_style))

    # Soil Recommendations
    story.append(Paragraph("Soil Health Recommendations", h2_style))
    for tip in [
        "Test soil pH before planting (target 6.0–7.0 for most crops)",
        "Add 5cm compost annually to improve structure and water retention",
        "Use cover crops (legumes) in winter to fix nitrogen",
        "Avoid compaction — use raised beds or permanent paths",
        "Apply organic matter to improve sandy/clay soils"
    ]:
        story.append(Paragraph(f"• {tip}", body_style))

    # Pest & Disease Alerts
    story.append(Paragraph("Seasonal Pest & Disease Alerts", h2_style))
    story.append(Table([
        ["Season", "Pests/Diseases", "Mitigation"],
        ["Spring (Sep–Nov)", "Aphids, Whitefly", "Neem oil spray, companion planting"],
        ["Summer (Dec–Feb)", "Fungal disease (heat)", "Improve airflow, avoid overhead irrigation"],
        ["Autumn (Mar–May)", "Bollworm, Cutworm", "Pheromone traps, Bacillus thuringiensis"],
        ["Winter (Jun–Aug)", "Root rot (waterlogging)", "Improve drainage, reduce irrigation"],
    ], style=TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CREAM, colors.white]),
        ('PADDING', (0,0), (-1,-1), 6),
    ])))

    # Footer / Data Sources
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width="100%", color=LIGHT_GREEN, thickness=1))
    story.append(Paragraph("Data Sources", h2_style))
    for src in ["OpenTopography (SRTM Elevation Data)", "Climate Engine API (Climate Data)", "Sentinel Hub (Vegetation/NDVI)"]:
        story.append(Paragraph(f"• {src}", body_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("© 2026 Plantaah · plantaah.eco · hello@plantaah.eco", center_style))

    doc.build(story)
    return buffer.getvalue()


async def run_analysis(submission_id: str, submission: dict):
    """Run the full analysis pipeline for a submission."""
    submissions_db[submission_id]['status'] = 'processing'
    logger.info(f"Starting analysis for submission {submission_id}")

    try:
        polygon_coords = submission['polygon']['coordinates']

        # Run API calls in parallel with retry logic
        topo_task = fetch_with_retry(fetch_topography(polygon_coords))
        climate_task = fetch_with_retry(fetch_climate(polygon_coords))
        veg_task = fetch_with_retry(fetch_vegetation(polygon_coords))

        topography, climate, vegetation = await asyncio.gather(
            topo_task, climate_task, veg_task
        )

        crop_recs = generate_crop_recommendations(climate, vegetation, topography)
        planting_calendar = generate_planting_calendar(climate)

        analysis_data = {
            "topography": topography,
            "climate": climate,
            "vegetation": vegetation,
            "crop_recommendations": crop_recs,
            "planting_calendar": planting_calendar
        }

        # Generate PDF
        pdf_bytes = await generate_pdf_guide(submission, analysis_data)
        pdf_filename = f"{submission['project_name'].replace(' ', '_')}_eco_farming_guide_2026.pdf"

        # In production: upload to S3 here
        # For MVP: store in-memory reference
        pdf_url = f"/guides/{submission_id}/{pdf_filename}"

        submissions_db[submission_id].update({
            'status': 'completed',
            'analysis_data': analysis_data,
            'pdf_url': pdf_url,
            'completed_at': datetime.now(timezone.utc).isoformat()
        })

        logger.info(f"Analysis completed for submission {submission_id}")

        # In production: send email here via SendGrid
        # For MVP: log the action
        logger.info(f"Would send guide to {submission['email']} — PDF size: {len(pdf_bytes)} bytes")

    except Exception as e:
        logger.error(f"Analysis failed for {submission_id}: {e}")
        submissions_db[submission_id].update({
            'status': 'failed',
            'error_message': str(e),
            'completed_at': datetime.now(timezone.utc).isoformat()
        })


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Plantaah API", "version": "1.0.0"}


@app.post("/submit-analysis")
async def submit_analysis(req: SubmissionRequest):
    submission_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    submission = {
        "id": submission_id,
        "project_name": req.project_name,
        "email": req.email,
        "polygon": req.polygon.model_dump(),
        "area_hectares": req.area_hectares,
        "status": "pending",
        "analysis_data": None,
        "pdf_url": None,
        "created_at": now,
        "completed_at": None,
        "error_message": None
    }
    submissions_db[submission_id] = submission

    # Run analysis in background
    asyncio.create_task(run_analysis(submission_id, submission))

    return {
        "submission_id": submission_id,
        "status": "pending",
        "message": f"Analysis started. Guide will be emailed to {req.email} in 5-10 minutes."
    }


@app.get("/admin/submissions")
async def get_submissions(status: Optional[str] = None):
    items = list(submissions_db.values())
    if status:
        items = [s for s in items if s['status'] == status]
    items.sort(key=lambda x: x['created_at'], reverse=True)
    return items


@app.get("/admin/export")
async def export_submissions():
    items = list(submissions_db.values())

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "project_name", "email", "area_hectares", "status", "created_at", "completed_at", "error_message"])

    for s in items:
        writer.writerow([
            s.get('id'), s.get('project_name'), s.get('email'),
            s.get('area_hectares'), s.get('status'),
            s.get('created_at'), s.get('completed_at'), s.get('error_message', '')
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=plantaah_submissions.csv"}
    )


# Serve Vue.js frontend in production (when frontend/dist exists)
_frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if _frontend_dist.exists():
    from fastapi.responses import FileResponse

    app.mount("/assets", StaticFiles(directory=str(_frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        index = _frontend_dist / "index.html"
        return FileResponse(str(index))
