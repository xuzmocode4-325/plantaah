# planta
Geospatial analytics driven eco-agriculture AI # Product Requirements Document (PRD)

## **Planta Eco-Farming Context Analyzer**

***

### **1. Executive Summary**

| Attribute | Description |
|-----------|-------------|
| **Product Name** | Planta Eco-Farming Context Analyzer |
| **Version** | 1.0 (Draft) |
| **Target Launch** | Q3 2026 |
| **Owner** | Planta Team |
| **Problem** | Landscape architects and ecological farmers lack quick, automated access to site-specific contextual analysis data needed for eco-farming design decisions [1][2] |
| **Solution** | Single-page app that accepts minimal input (project name, email, polygon boundary), automates 90% of contextual analysis via APIs, and delivers a free 1-year personalized eco-farming guide via email [3][4][5] |
| **Value Proposition** | "Get your site-specific eco-farming guide in 5 minutes—no manual data collection required" |

***

### **2. Goals & Success Metrics**

| Goal | Metric | Target |
|------|--------|--------|
| **User adoption** | Monthly active users (MAU) | 1,000 by Month 6 |
| **Conversion** | Email sign-up completion rate | ≥75% |
| **Automation** | % of contextual analysis steps automated | ≥90% [3][4] |
| **Engagement** | Guide download rate | ≥60% |
| **Retention** | 30-day repeat user rate | ≥25% |
| **Performance** | Analysis completion time | ≤5 minutes |
| **Quality** | API success rate (topography + climate + vegetation) | ≥95% |

***

### **3. User Personas**

#### **Primary: Ecological Farmer (60% of users)**
| Attribute | Details |
|-----------|---------|
| **Demographics** | Rurual & Suburban area dwellers (ZA, initially, eventually worldwide) |
| **Goals** | Start eco-farming on new land, optimize crop selection, understand soil/climate constraints |
| **Constraints** | Limited budget, no GIS expertise, needs quick actionable insights |
| **Tech proficiency** | Medium (uses email, mobile apps, basic web) |
| **Triggers** | "I just bought land—what should I grow?" |

#### **Secondary: Landscape Architect (40% of users)**
| Attribute | Details |
|-----------|---------|
| **Goals** | Rapid site analysis for early design phase, validate ecological feasibility |
| **Constraints** | Tight project timelines, needs data to support design decisions |
| **Tech proficiency** | High (uses CAD, GIS, professional tools) |
| **Triggers** | "Client needs site feasibility in 2 days" |

***

### **4. User Stories**

| ID | User Story | Priority |
|----|------------|----------|
| **US-1** | As a farmer, I want to draw my property boundary on a map and get my eco-farming guide emailed to me in under 5 minutes | P0 |
| **US-2** | As a farmer, I want the guide to include specific crops suitable for my climate, soil, and water conditions | P0 |
| **US-3** | As a landscape architect, I want to export the contextual analysis data (topography, vegetation, climate) for my design software | P1 |
| **US-4** | As a user, I want to see my polygon boundary clearly drawn and validated before submitting | P0 |
| **US-5** | As a user, I want to receive a confirmation email with my guide attachment within 10 minutes of submission | P0 |
| **US-6** | As a user, I want the app to work on mobile so I can draw my boundary while on my property | P1 |
| **US-7** | As a user, I want to know what data sources power my analysis (transparency) | P2 |

***

### **5. Functional Requirements**

#### **5.1 Onboarding & Input Collection (FR-1)**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **FR-1.1** | Single-page landing with minimal form: project name, email, polygon drawing | P0 |
| **FR-1.2** | Interactive map UI with Leaflet/Mapbox for drawing polygon boundary (minimum 4 points) | P0 |
| **FR-1.3** | Real-time polygon validation: show area (hectares), warn if <0.1 ha or >500 ha | P0 |
| **FR-1.4** | Coordinate auto-capture from polygon (lat/lon decimal format) | P0 |
| **FR-1.5** | Email validation (regex + real-time check) | P0 |
| **FR-1.6** | "Submit for Analysis" button with loading state (spinner + progress messages) | P0 |
| **FR-1.7** | Success screen: "Your guide is being generated! Check your email in 5-10 minutes" | P0 |

#### **5.2 Automated Contextual Analysis (FR-2)**

| Requirement | Description | Priority | API Source |
|-------------|-------------|----------|------------|
| **FR-2.1** | **Topography**: Fetch elevation DEM, generate contours, slope analysis, elevation range | P0 | OpenTopography API [4][6] |
| **FR-2.2** | **Climate**: Generate site characterization report (temperature, rainfall, drought risk, wind) | P0 | Climate Engine API [3][7] |
| **FR-2.3** | **Vegetation**: Calculate NDVI, fractional vegetation cover, vegetation area | P0 | Sentinel Hub API [8][5] |
| **FR-2.4** | **Zoning/Land Use**: Fetch land use classification, zoning overlay (if available) | P1 | ArcGIS API for Python [9][10] |
| **FR-2.5** | **Water**: Infer water availability from climate data (rainfall, drought indices) | P0 | Climate Engine drought endpoint [3] |
| **FR-2.6** | **Soil**: Infer soil type from satellite data + regional soil maps (limited accuracy) | P1 | Sentinel Hub + ArcGIS [5] |
| **FR-2.7** | Run all API calls in parallel (reduce wait time) | P0 | N/A |
| **FR-2.8** | Retry failed API calls (max 3 attempts, 5-second delay) | P0 | N/A |
| **FR-2.9** | Log all API requests/responses for debugging | P1 | N/A |

#### **5.3 Eco-Farming Guide Generation (FR-3)**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **FR-3.1** | Generate 12-month personalized eco-farming guide (PDF) based on analysis data | P0 |
| **FR-3.2** | Guide content includes: <br>-  Crop recommendations (suitable crops by season) <br>-  Water management strategy <br>-  Soil health tips <br>-  Planting calendar <br>-  Pest/disease warnings <br>-  Climate risks & mitigation | P0 |
| **FR-3.3** | Guide template uses user's polygon area, climate data, vegetation data, elevation | P0 |
| **FR-3.4** | PDF generated via Python library (ReportLab or FPDF) | P0 |
| **FR-3.5** | Guide file named: `{project_name}_eco_farming_guide_2026.pdf` | P0 |
| **FR-3.6** | Store PDF in cloud storage (AWS S3 / Google Cloud Storage) with 1-year retention | P1 |
| **FR-3.7** | Generate HTML preview of guide (for email body) | P1 |

#### **5.4 Email Delivery (FR-4)**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **FR-4.1** | Send email via SMTP service (SendGrid / AWS SES) within 10 minutes of analysis completion | P0 |
| **FR-4.2** | Email subject: "🌱 Your personalized eco-farming guide for {project_name}" | P0 |
| **FR-4.3** | Email body: HTML preview + PDF attachment + "Download again" link | P0 |
| **FR-4.4** | Email template includes: <br>-  Welcome message <br>-  Key insights summary (top 3 crops, water strategy) <br>-  PDF attachment <br>-  Footer with Planta contact + privacy link | P0 |
| **FR-4.5** | Email delivery retry (max 2 attempts) | P1 |
| **FR-4.6** | Track email open rate + PDF download rate (via email analytics) | P2 |

#### **5.5 Admin Dashboard (FR-5)**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| **FR-5.1** | Admin view: list all submissions (project name, email, date, status) | P2 |
| **FR-5.2** | Filter by status (pending / completed / failed) | P2 |
| **FR-5.3** | View individual analysis data (topography, climate, vegetation JSON) | P2 |
| **FR-5.4** | Export submission data (CSV) | P2 |

***

### **6. Non-Functional Requirements**

| Category | Requirement | Target |
|----------|-------------|--------|
| **Performance** | End-to-end analysis + email delivery time | ≤5 minutes |
| **Performance** | API response time (single call) | ≤2 seconds |
| **Performance** | Page load time (Vue app) | ≤1 second |
| **Scalability** | Concurrent users supported | 100 |
| **Reliability** | System uptime | ≥99% |
| **Security** | Email data encrypted in transit | TLS 1.3 |
| **Security** | API keys stored in environment variables | Never in code |
| **Security** | GDPR compliance: email opt-out, data deletion request | Required |
| **Accessibility** | WCAG 2.1 AA compliance (form labels, keyboard navigation) | Required |
| **Mobile** | Responsive design (iOS/Android Chrome, Safari) | Required |
| **Cost** | Monthly infrastructure cost (AWS/serverless) | ≤$500 for 10K users |

***

### **7. Technical Architecture**

#### **7.1 Tech Stack**

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Vue.js 3 (ECMAScript) | UI components, polygon drawing, form validation |
| **Frontend Map** | Leaflet.js (open-source) or Mapbox GL JS | Interactive polygon drawing UI |
| **Backend** | Python 3.11 + FastAPI | Serverless function APIs (AWS Lambda / Google Cloud Functions) |
| **API Gateway** | AWS API Gateway / Google Cloud Endpoints | Route requests to Lambda functions |
| **Storage** | AWS S3 / Google Cloud Storage | Store PDF guides, log analysis data |
| **Email** | SendGrid (free tier) or AWS SES | Email delivery |
| **Database** | PostgreSQL (Supabase) or MongoDB Atlas | Store user submissions, project data |
| **Authentication** | None (no login required for MVP) | Optional for v2 |
| **CI/CD** | GitHub Actions | Automated testing, deployment |
| **Monitoring** | AWS CloudWatch / Google Cloud Logging | Error tracking, API metrics |

#### **7.2 Serverless Function Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Vue.js Frontend (CDN)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ Landing Page│  │ Polygon Map  │  │ Success Screen  │    │
│  └─────────────┘  └──────────────┘  └─────────────────┘    │
│         │                    │                    │          │
│         └────────────────────┴────────────────────┘          │
│                              │                               │
│                    POST /submit-analysis                     │
│                              │                               │
└──────────────────────────────┼───────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              AWS API Gateway (HTTPS)                         │
│                              │                               │
│                    route: /submit-analysis                   │
│                              │                               │
└──────────────────────────────┼───────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           Python Lambda Function (FastAPI)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. Validate input (email, polygon coordinates)      │   │
│  │ 2. Parallel API calls:                              │   │
│  │    • OpenTopography (elevation) [web:24]            │   │
│  │    • Climate Engine (climate) [web:18]              │   │
│  │    • Sentinel Hub (NDVI) [web:43]                   │   │
│  │ 3. Aggregate analysis data                          │   │
│  │ 4. Generate PDF eco-farming guide                   │   │
│  │ 5. Upload PDF to S3                                 │   │
│  │ 6. Send email via SendGrid                          │   │
│  │ 7. Store submission in database                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                              │                               │
└──────────────────────────────┼───────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
│ OpenTopo API│    │Climate Engine   │    │Sentinel Hub  │
│ [web:24]    │    │API [web:18]     │    │API [web:43]  │
└─────────────┘    └─────────────────┘    └──────────────┘
         │                     │                     │
         └─────────────────────┴─────────────────────┘
                               │
                               ▼
                ┌─────────────────────────┐
                │   AWS S3 (PDF storage)  │
                │   Supabase (DB)         │
                │   SendGrid (email)      │
                └─────────────────────────┘
```

#### **7.3 API Function Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/submit-analysis` | POST | Main submission: receives `{project_name, email, polygon}` |
| `/health` | GET | Health check for Lambda function |
| `/admin/submissions` | GET | Admin dashboard (protected by API key) |
| `/admin/export` | GET | Export submissions as CSV |

#### **7.4 Data Schema**

```python
# Submission model (PostgreSQL)
class Submission:
    id: UUID
    project_name: String
    email: String
    polygon: JSON  # [[lon, lat], [lon, lat], ...]
    area_hectares: Float
    status: Enum[pending, completed, failed]
    analysis_data: JSON  # {topography, climate, vegetation, water, soil}
    pdf_url: String  # S3 path
    created_at: DateTime
    completed_at: DateTime
    error_message: String  # if failed
```

***

### **8. User Flow**

```mermaid
graph TD
    A[User lands on Vue.js app] --> B[Enter project name]
    B --> C[Enter email address]
    C --> D[Draw polygon on map]
    D --> E{Polygon valid?}
    E -->|No| F[Show validation error: "Minimum 4 points"]
    F --> D
    E -->|Yes| G[Show area in hectares]
    G --> H[Click "Submit for Analysis"]
    H --> I[Loading screen with progress messages]
    I --> J{Lambda function executes}
    J -->|API calls parallel| K[OpenTopography + Climate Engine + Sentinel Hub]
    K --> L[Aggregate data + generate PDF]
    L --> M[Upload PDF to S3]
    M --> N[Send email via SendGrid]
    N --> O[Store submission in database]
    O --> P[Show success screen]
    P --> Q[User receives email in 5-10 minutes]
```

***

### **9. Eco-Farming Guide Template Structure**

The 12-month PDF guide includes:

| Section | Content | Data Source |
|---------|---------|-------------|
| **Cover Page** | Project name, user email, "1-Year Eco-Farming Guide" | User input |
| **Executive Summary** | Top 3 recommended crops, key climate risks, water strategy | Climate Engine + NDVI [3][5] |
| **Site Overview** | Map with polygon, area (ha), elevation range | OpenTopography [4] |
| **Climate Profile** | Temperature range, rainfall, drought risk, wind direction | Climate Engine [3] |
| **Vegetation Status** | NDVI score, vegetation cover %, bare land % | Sentinel Hub [5] |
| **Topography** | Slope class, contour map, elevation min/max | OpenTopography [4] |
| **Water Management** | Rainfall adequacy, irrigation strategy, drainage tips | Climate Engine drought [3] |
| **Soil Recommendations** | Soil type inference, health tips, amendments | Climate Engine + regional data [3] |
| **Monthly Planting Calendar** | Month-by-month crop recommendations (12 months) | Climate data + crop database |
| **Seasonal Crop Guide** | Spring/Summer/Autumn/Winter crops with details | Climate Engine [3] |
| **Pest & Disease Alerts** | Seasonal warnings based on climate | Climate data |
| **Climate Risks** | Drought, frost, heatwave mitigation | Climate Engine [3] |
| **Data Sources** | List of APIs used (OpenTopography, Climate Engine, Sentinel Hub) | N/A |
| **Back Page** | Planta contact, "Download again" link, privacy policy | N/A |

***

### **10. MVP Scope & Phasing**

#### **Phase 1: MVP (Q3 2026)**
| Feature | Description |
|---------|-------------|
| ✅ Single-page Vue.js app with polygon drawing | Leaflet.js map |
| ✅ Minimal form (project name, email, polygon) | No login required |
| ✅ 3 API integrations | OpenTopography, Climate Engine, Sentinel Hub |
| ✅ PDF guide generation | ReportLab/FPDF |
| ✅ Email delivery | SendGrid free tier |
| ✅ Basic admin dashboard | Submissions list |
| ✅ Error handling + retries | For failed API calls |

#### **Phase 2: v2 (Q4 2026)**
| Feature | Description |
|---------|-------------|
| 🔄 ArcGIS zoning integration | Land use classification |
| 🔄 Mobile app (Vue + native) | iOS/Android |
| 🔄 User accounts | Save projects, re-download guides |
| 🔄 Guide customization | User selects crop preferences |
| 🔄 Email analytics | Open rate, download rate tracking |
| 🔄 Export analysis data | CSV/JSON download |

#### **Phase 3: v3 (Q1 2027)**
| Feature | Description |
|---------|-------------|
| 🚀 Google Vision API for image uploads | Object detection from site photos |
| 🚀 View analysis (3D Isovist) | ArcGIS view cones |
| 🚀 Real-time soil data | Integration with soil databases |
| 🚀 Multi-language support | English, Afrikaans, Xhosa |

***

### **11. Risk Assessment**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **API rate limits** (OpenTopography/Climate Engine) | Medium | High | Implement request queuing, cache results, use free tier with monitoring |
| **API failures** (timeout, 500 errors) | Medium | High | Retry logic (3 attempts), fallback to cached data, log errors |
| **Email not delivered** | Low | Medium | SendGrid retry, SMS fallback (v2), user notification |
| **Polygon drawing too complex** | Low | Medium | Simplify UI, add guided tutorial, mobile-optimized touch |
| **PDF generation fails** | Low | Medium | Template validation, fallback to basic HTML email |
| **Data privacy violation** | Low | High | GDPR compliance, encrypted storage, opt-out mechanism |
| **Cost exceeds budget** | Medium | Medium | Monitor API usage, set AWS budget alerts, optimize parallel calls |
| **Guide quality low** | Medium | High | Test with 10 users, iterate on crop database, add expert review |

***

### **12. Dependencies**

| Dependency | Owner | Status |
|------------|-------|--------|
| **OpenTopography API access** | OpenTopography | ✅ Free tier available [4] |
| **Climate Engine API access** | Climate Engine | ✅ Free tier available [3][11] |
| **Sentinel Hub API access** | Sinergise | ✅ Free tier available [5] |
| **SendGrid email service** | SendGrid | ✅ Free tier (100 emails/day) |
| **AWS Lambda / Cloud Functions** | AWS / Google | ✅ Setup required |
| **Supabase / MongoDB Atlas** | Supabase / MongoDB | ✅ Free tier available |
| **Vue.js + Leaflet** | Open-source | ✅ No setup needed |

***

### **13. Open Questions**

| Question | Decision Needed |
|----------|-----------------|
| Should we require user login for v2 (save projects)? | Product team |
| What crop database to use for planting calendar? | Agronomy expert |
| Should PDF include interactive links (download again)? | Design team |
| How to handle users outside Cape Town (different climate zones)? | Engineering team |
| Budget for AWS costs beyond free tier? | Finance team |

***

### **14. Approval**

| Role | Name | Status | Date |
|------|------|--------|------|
| **Product Owner** | [Pending] | 🟡 Draft | June 22, 2026 |
| **Engineering Lead** | [Pending] | 🟡 Pending | — |
| **Design Lead** | [Pending] | 🟡 Pending | — |
| **Agronomy Advisor** | [Pending] | 🟡 Pending | — |

***

## **Appendix: Minimal Input JSON Schema**

```json
{
  "project_name": "string (required, min 3 chars)",
  "email": "string (required, valid email format)",
  "polygon": {
    "type": "Polygon",
    "coordinates": [
      [
        [lon1, lat1],
        [lon2, lat2],
        [lon3, lat3],
        [lon4, lat4]
      ]
    ]
  },
  "area_hectares": "number (calculated, min 0.1, max 500)"
}
```

***

**Document Status**: Draft  
**Last Updated**: June 22, 2026  
**Next Review**: July 1, 2026 (after stakeholder feedback)

Sources
[1] Contextual Analysis for Architects | PDF | Information https://www.scribd.com/document/710499928/SITE-ANALYSIS
[2] Site Analysis https://books.google.com/books/about/Site_Analysis.html?id=F0PNMKek-1AC
[3] Reports Endpoints - ClimateEngine.org https://www.climateengine.org/apis/reportsEndpoints/
[4] OpenTopography API https://portal.opentopography.org/apidocs/
[5] Sentinel Hub - Atlas https://atlas.co/data-sources/sentinel-hub/
[6] API access to USGS 3DEP rasters now available - OpenTopography https://opentopography.org/news/api-access-usgs-3dep-rasters-now-available
[7] Demos - ClimateEngine.org https://www.climateengine.org/apis/api-tutorials/
[8] Vegetation area https://forum.sentinel-hub.com/t/vegetation-area/3105
[9] ArcGIS API for Python https://pro.arcgis.com/en/pro-app/3.4/arcpy/get-started/arcgis-api-for-python.htm
[10] Scripting with ArcGIS Python API https://enterprise.arcgis.com/en/portal/10.8/use/scripting-with-the-arcgis-python-api.htm
[11] Get Started - ClimateEngine.org https://www.climateengine.org/get_started/get-started/
