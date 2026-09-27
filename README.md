# DRIVYAM: AI-Enabled Capacity Building Platform for India's Official Statistical System

[![Smart India Hackathon 2024](https://img.shields.io/badge/SIH%20Problem%20Statement-SIH26101-orange.svg)](https://sih.gov.in)
[![MoSPI Official Cadres](https://img.shields.io/badge/Target%20Cadres-ISS%20%7C%20SSS-blue.svg)](https://mospi.gov.in)
[![iGOT Karmayogi](https://img.shields.io/badge/Integration-iGOT%20Karmayogi%20Bharat-green.svg)](https://karmayogi.gov.in)
[![Tests Passing](https://img.shields.io/badge/Tests-8%20Passed-brightgreen.svg)]()

> **DRIVYAM** (*द्रिव्यम्*) is an end-to-end, production-grade AI capacity building platform designed for the **Ministry of Statistics and Programme Implementation (MoSPI)** to strengthen India's Official Statistical System across the **Indian Statistical Service (ISS)** and **Subordinate Statistical Service (SSS)**.

---

## 🏛️ Executive Summary & SIH26101 Alignment

In India's official statistical apparatus, statistical officers routinely execute critical statutory mandates—such as compiling the **System of National Accounts (SNA 2008)**, administering the **Periodic Labour Force Survey (PLFS)**, and calculating **Consumer Price Indices (CPI)**. 

**DRIVYAM** directly solves Problem Statement **SIH26101** by delivering:
1. **Government of India FRAC Competency Gap Engine**: Evaluates officers across Domain, Functional, and Behavioural competencies against Level 1–5 benchmarks, generating dynamic multi-axis Radar Gap Charts.
2. **Deficit-Prioritized iGOT Karmayogi Adapter**: Discovers and recommends authentic MoSPI courses on Karmayogi Bharat prioritized by statutory criticality weights (`Priority = Gap × Weight`).
3. **Zero-Hallucination RAG Assessment Generator**: Ingests official MoSPI statistical manuals (PDF/DOCX), vectors them in ChromaDB, and generates 4-tier Bloom's Taxonomy MCQs with exact page citations and excerpts.
4. **Dual-Portal Workflow**: Features a dedicated **Cadre Learner Portal** with interactive timer-based testing and a **MoSPI Trainer Ingestion Studio** with cadre-wide capacity analytics.

---

## 📐 System Architecture

```mermaid
flowchart TD
    subgraph Ingestion ["1. Document Ingestion & RAG Indexing"]
        A[Official MoSPI Manuals<br/>PLFS, SNA 2008, CPI, ASI] --> B[RAG Engine<br/>PyPDF Text Extraction & Chunking]
        B --> C[(ChromaDB Vector Store<br/>Deterministic Embeddings)]
    end

    subgraph FRAC ["2. FRAC Framework & Gap Engine"]
        D[Cadre Benchmarks<br/>ISS & SSS Roles] --> E[FRAC Engine]
        F[Officer Assessed Scores<br/>Levels 1 - 5] --> E
        E --> G[Multi-Axis Radar Data]
        E --> H[Readiness Index Ω<br/>0% - 100%]
    end

    subgraph IGOT ["3. iGOT Karmayogi Bharat Adapter"]
        E --> I[Deficit Priority Matrix<br/>Gap × Criticality Weight]
        I --> J[Karmayogi Course Matcher]
        J --> K[Personalized Course Cards<br/>Direct iGOT Enrolment Links]
    end

    subgraph Assessment ["4. Bloom's Taxonomy Assessment"]
        C --> L[Quiz Generator]
        L --> M[4-Tier Bloom's MCQs<br/>Remembering | Understanding | Applying | Analyzing]
        M --> N[Quiz Player & Timer]
        N --> O[Verified Document Citations<br/>Page & Section Coordinates]
        N --> P[Automated Competency Uplift<br/>Dynamic Score Adjustment]
        P -.-> F
    end
```

---

## 🔬 Mathematical Formulas

### 1. Competency Gap Formula
$$\text{Gap}_i = \max(0, \text{Target Level}_i - \text{Current Level}_i)$$

### 2. Departmental Readiness Index ($\Omega$)
$$\Omega = \left(\frac{\sum_{i=1}^{N} w_i \times \min\left(1.0, \frac{\text{Current Level}_i}{\text{Target Level}_i}\right)}{\sum_{i=1}^{N} w_i}\right) \times 100$$
Where:
- $w_i$: Criticality weight assigned to competency $i$ (e.g., $1.5$ for statutory sampling duties).
- $\text{Target Level}_i$: Benchmark target required for the cadre role (Levels 1 to 5).
- $\text{Current Level}_i$: Officer's evaluated baseline or test-proven score.

### 3. Training Recommendation Priority Score
$$\text{Priority Score}_i = \text{Gap}_i \times w_i$$

---

## 🌟 Key Capabilities

| Capability | Official MoSPI Standard | DRIVYAM Implementation |
|---|---|---|
| **Ontology** | GoI FRAC Framework | Roles, Activities, Domain/Functional/Behavioural Competencies (Levels 1–5) |
| **iGOT Integration** | Karmayogi Bharat Platform | Deficit-prioritized recommendation adapter with direct course links |
| **Grounding** | Official Manuals (PLFS, CPI, SNA) | Exact page and section citations with zero LLM hallucination |
| **Cognitive Scale** | Bloom's Taxonomy | Multi-tier distribution: Remembering (20%), Understanding (30%), Applying (30%), Analyzing (20%) |
| **Radar Chart** | Recharts Visualizer | Multi-axis SVG radar showing assessed levels against role benchmarks |
| **Deployment** | Meghraj Cloud Ready | Docker Compose orchestration with PostgreSQL/SQLite & ChromaDB |

---

## 🚀 Quick Start Guide

### Option 1: One-Click Demo Initialization (Recommended)

Run the automated demo script from the project root:

```bash
chmod +x scripts/demo_setup.sh
./scripts/demo_setup.sh
```

This script:
1. Verifies the Python 3.11+ virtual environment
2. Executes the full test suite (`pytest`)
3. Checks frontend packages
4. Prints instructions for immediate evaluation

---

### Option 2: Running Locally in Development Mode

#### 1. Backend Server (FastAPI)
```bash
# Activate virtual environment
source .venv/bin/activate

# Start API on port 8000
PYTHONPATH=. uvicorn backend.app.main:app --port 8000 --reload
```
- **Backend API**: `http://localhost:8000`
- **Swagger Documentation**: `http://localhost:8000/docs`

#### 2. Frontend Application (Next.js 14)
```bash
cd frontend
npm run dev
```
- **Cadre Dashboard**: `http://localhost:3000/dashboard`
- **FRAC Diagnostic**: `http://localhost:3000/diagnostic`
- **Bloom's Assessment**: `http://localhost:3000/assessment/demo`
- **MoSPI Admin Studio**: `http://localhost:3000/admin`

---

### Option 3: Containerized Launch (Docker Compose)

```bash
docker-compose up --build
```
Launches both services in isolated Docker containers:
- Frontend on `http://localhost:3000`
- Backend on `http://localhost:8000`

---

## 🧪 Comprehensive End-to-End Verification

To verify all 7 phases of the system lifecycle against a live running app:

```bash
PYTHONPATH=. .venv/bin/python tests/e2e_verification.py
```

### Verification Pipeline Checklist:
- [x] **Step 0**: Database Schema Initialization & MoSPI Seed Population
- [x] **Phase 1**: Health Check & SSS/ISS Officer Authentication
- [x] **Phase 2**: FRAC Competency Gap Radar Generation (`7 Axes`)
- [x] **Phase 3**: Deficit-Prioritized iGOT Karmayogi Course Recommendations
- [x] **Phase 4**: Ingesting MoSPI Manual & ChromaDB Vectorization
- [x] **Phase 5**: 4-Tier Bloom's Taxonomy Quiz Generation with Page Citations
- [x] **Phase 6**: Assessment Submission, Grading & Competency Score Uplift (`L2.2 -> L2.5`)
- [x] **Phase 7**: Post-Test Readiness Index Improvement Validation (`78.5% -> 79.9%`)

---

## 📂 Project Structure

```
drishyam/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI REST Routers (auth, competencies, igot, documents, quizzes)
│   │   ├── core/            # Config, database engine, JWT security
│   │   ├── models/          # SQLAlchemy 2.0 ORM models
│   │   ├── schemas/         # Pydantic v2 schemas
│   │   ├── services/        # FRAC Engine, iGOT Client, RAG Engine, Quiz Generator
│   │   ├── data/seeds/      # Authentic MoSPI Cadre seed data
│   │   └── main.py          # FastAPI application entrypoint with CORS
│   ├── tests/               # Pytest test suite (8 tests, 100% passing)
│   ├── Dockerfile           # Backend container build
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── dashboard/   # Cadre Officer Radar Dashboard
│   │   │   ├── diagnostic/  # FRAC Baseline Intake Quiz
│   │   │   ├── assessment/  # Bloom's Quiz Player with Citations
│   │   │   ├── admin/       # MoSPI Admin Ingestion Studio & Analytics
│   │   │   ├── layout.tsx   # Root Layout with MoSPI branding
│   │   │   └── page.tsx     # Hero Gateway
│   │   ├── components/      # Recharts Radar, Citation Viewer, Uploader, Cards
│   │   └── lib/             # Typed API client
│   ├── Dockerfile           # Frontend container build
│   ├── package.json         # Next.js 14, Tailwind CSS, Lucide, Recharts
│   └── tailwind.config.js   # MoSPI Navy & Saffron design system
├── tests/
│   └── e2e_verification.py  # 7-Phase End-to-End System Test
├── scripts/
│   └── demo_setup.sh        # One-click evaluation launch script
├── drivyam.pdf              # 6-Page Executive Blueprint & Technical Specification
├── docker-compose.yml       # Production container orchestration
└── README.md                # Hackathon pitch & technical documentation
```

---

## 👥 Hackathon Team & Acknowledgements

Developed for **Smart India Hackathon 2024** under Problem Statement **SIH26101**.
Special thanks to the **Ministry of Statistics and Programme Implementation (MoSPI)** and **Karmayogi Bharat (DoPT)** for the open competency frameworks and official statistical guidelines.
