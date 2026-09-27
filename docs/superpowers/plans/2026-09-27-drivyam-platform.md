# Project Drivyam (SIH26101) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and integrate DRIVYAM, an AI-enabled learning & capacity building platform for India's Official Statistical System (MoSPI) that identifies FRAC competency gaps, recommends personalized iGOT Karmayogi courses, and generates verified Bloom's taxonomy quizzes with document citations from uploaded statistical manuals.

**Architecture:** A high-performance Python FastAPI backend delivering FRAC competency analytics, iGOT Karmayogi course matching, and LangChain/ChromaDB RAG quiz generation, coupled with a responsive Next.js 14 App Router frontend featuring dynamic Recharts radar visualizations and interactive assessment players.

**Tech Stack:** 
- Backend: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0, ChromaDB, LangChain, PyPDF, pytest
- Frontend: Next.js 14 (App Router), React 18, Tailwind CSS, Lucide React, Recharts
- Database: SQLite (local testing & zero-setup demo) / PostgreSQL (production & Docker)
- Orchestration: Docker Compose, NIC Meghraj Cloud aligned

**Spec:** [`docs/superpowers/specs/2026-09-27-sih26101-karmayogi-stat-platform-design.md`](file:///home/shiv/Sandilyapoorv/drishyam/docs/superpowers/specs/2026-09-27-sih26101-karmayogi-stat-platform-design.md)

## Global Constraints
- Target Official Cadres: Indian Statistical Service (ISS), Subordinate Statistical Service (SSS), State DES, Field Enumerators
- Competency Taxonomy: GoI FRAC Framework (Domain, Functional, Behavioural across Levels 1–5)
- Quiz Requirement: Bloom's Revised Taxonomy (Levels 1–4) with strict page/section citations from source manuals
- iGOT Karmayogi: Standards-compliant adapter supporting both sandbox catalog and live API endpoint configuration

## Review Focus
1. Malformed or empty uploaded documents must fail gracefully without crashing the RAG vector indexing pipeline.
2. An officer taking a diagnostic quiz with 0 correct answers must receive valid Level 1 baseline scores and actionable Level 1 iGOT recommendations rather than division-by-zero or empty lists.
3. Competency radar gap calculation must accurately clamp gaps between 0 and 5 (`Gap = max(0, Target - Current)`).
4. Quiz grading must reject duplicate submissions and correctly calculate percentage scores.
5. All generated MCQs must have exactly 4 choices, a valid 0-3 answer index, an explanation, and source citations.

---

### Task 1: Backend Scaffolding, Core Config & Dependencies

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/app/__init__.py`
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/database.py`
- Test: `backend/tests/test_config.py`

**Interfaces:**
- Produces: `settings` (pydantic-settings), `engine`, `SessionLocal`, `Base` (SQLAlchemy declarative base)

- [ ] **Step 1: Write backend requirements and setup virtual environment**
- [ ] **Step 2: Write failing test for config and database connection**
- [ ] **Step 3: Implement `config.py` and `database.py`**
- [ ] **Step 4: Run pytest and verify passes**
- [ ] **Step 5: Commit changes**

---

### Task 2: Database Models & Official MoSPI Seed Data

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/competency.py`
- Create: `backend/app/models/user.py`
- Create: `backend/app/models/document.py`
- Create: `backend/app/models/quiz.py`
- Create: `backend/app/models/igot.py`
- Create: `backend/app/data/seeds/mospi_data.py`
- Test: `backend/tests/test_models_and_seeds.py`

**Interfaces:**
- Produces: `CadreRole`, `Competency`, `RoleBenchmark`, `User`, `UserCompetencyScore`, `Document`, `Quiz`, `QuizQuestion`, `QuizAttempt`, `IgotCourse`
- Function: `seed_database(db: Session)` to populate official ISS/SSS roles, FRAC competencies, and sample iGOT courses

- [ ] **Step 1: Write failing test for model creation and seed population**
- [ ] **Step 2: Implement SQLAlchemy ORM models**
- [ ] **Step 3: Implement `mospi_data.py` with authentic MoSPI cadre benchmarks (ISS, SSS, DES) and iGOT courses**
- [ ] **Step 4: Run pytest and verify seeds load cleanly**
- [ ] **Step 5: Commit changes**

---

### Task 3: FRAC Competency Gap Engine

**Files:**
- Create: `backend/app/schemas/competency.py`
- Create: `backend/app/services/frac_engine.py`
- Test: `backend/tests/test_frac_engine.py`

**Interfaces:**
- Consumes: `RoleBenchmark`, `UserCompetencyScore`, `Competency`
- Produces: 
  - `calculate_competency_gaps(target_benchmarks, current_scores) -> List[CompetencyGap]`
  - `calculate_readiness_index(target_benchmarks, current_scores) -> float`
  - `format_radar_chart_data(target_benchmarks, current_scores) -> List[RadarAxisItem]`
  - `evaluate_diagnostic_test(answers, question_mappings) -> Dict[str, float]`

- [ ] **Step 1: Write failing tests for FRAC gap scoring and radar chart transformations**
- [ ] **Step 2: Implement Pydantic schemas in `schemas/competency.py`**
- [ ] **Step 3: Implement `services/frac_engine.py` with mathematical gap computation & radar matrix**
- [ ] **Step 4: Run pytest and verify mathematical accuracy**
- [ ] **Step 5: Commit changes**

---

### Task 4: iGOT Karmayogi Adapter Service

**Files:**
- Create: `backend/app/schemas/igot.py`
- Create: `backend/app/services/igot_client.py`
- Test: `backend/tests/test_igot_client.py`

**Interfaces:**
- Consumes: `List[CompetencyGap]` from Task 3
- Produces:
  - `IgotClient.recommend_courses(user_gaps: List[CompetencyGap], limit: int = 5) -> List[IgotCourseRecommendation]`
  - `IgotClient.get_catalog(competency_type: Optional[str] = None) -> List[IgotCourseSchema]`

- [ ] **Step 1: Write failing tests for iGOT course matching and ranking**
- [ ] **Step 2: Implement Pydantic schemas in `schemas/igot.py`**
- [ ] **Step 3: Implement `services/igot_client.py` with gap-severity ranking and deep links**
- [ ] **Step 4: Run pytest and verify course recommendations correctly target deficit competencies**
- [ ] **Step 5: Commit changes**

---

### Task 5: RAG Document Ingestion & Vector Indexing Engine

**Files:**
- Create: `backend/app/schemas/document.py`
- Create: `backend/app/services/rag_engine.py`
- Test: `backend/tests/test_rag_engine.py`

**Interfaces:**
- Produces:
  - `ingest_document(file_bytes: bytes, filename: str, doc_id: str) -> DocumentMetadata`
  - `retrieve_relevant_chunks(query: str, doc_id: Optional[str] = None, top_k: int = 4) -> List[DocumentChunk]`

- [ ] **Step 1: Write failing tests for PDF text extraction, chunking, and vector storage/retrieval**
- [ ] **Step 2: Implement `services/rag_engine.py` using PyPDF/pdfplumber, RecursiveCharacterTextSplitter, and ChromaDB**
- [ ] **Step 3: Ensure chunks preserve metadata (page number, section name, document title)**
- [ ] **Step 4: Run pytest with a sample statistical guideline document**
- [ ] **Step 5: Commit changes**

---

### Task 6: Bloom's Taxonomy Quiz Generator & Scoring Service

**Files:**
- Create: `backend/app/schemas/quiz.py`
- Create: `backend/app/services/quiz_generator.py`
- Test: `backend/tests/test_quiz_generator.py`

**Interfaces:**
- Consumes: Document chunks from `rag_engine`
- Produces:
  - `generate_quiz_from_document(doc_id: str, num_questions: int = 5, bloom_distribution: Dict) -> Quiz`
  - `grade_quiz_attempt(quiz_id: str, answers: Dict[int, int]) -> QuizAttemptResult`
  - `update_competency_scores_from_attempt(user_id: str, attempt_result: QuizAttemptResult) -> Dict[str, float]`

- [ ] **Step 1: Write failing tests for quiz generation, citation verification, and grading**
- [ ] **Step 2: Implement `services/quiz_generator.py` with multi-tier Bloom's prompt engineering and robust fallback parser**
- [ ] **Step 3: Implement grading and automated competency score adjustment**
- [ ] **Step 4: Run pytest and verify Bloom's levels and citation formatting**
- [ ] **Step 5: Commit changes**

---

### Task 7: FastAPI REST Endpoints & Authentication

**Files:**
- Create: `backend/app/api/auth.py`
- Create: `backend/app/api/competencies.py`
- Create: `backend/app/api/igot.py`
- Create: `backend/app/api/documents.py`
- Create: `backend/app/api/quizzes.py`
- Create: `backend/app/main.py`
- Test: `backend/tests/test_api_endpoints.py`

**Interfaces:**
- Endpoints:
  - `POST /api/auth/login`, `GET /api/auth/me`
  - `GET /api/competencies/roles`, `GET /api/competencies/gap-analysis`, `POST /api/competencies/diagnostic`
  - `GET /api/igot/recommendations`, `GET /api/igot/catalog`
  - `POST /api/documents/upload`, `GET /api/documents`
  - `POST /api/quizzes/generate`, `GET /api/quizzes`, `GET /api/quizzes/{id}`, `POST /api/quizzes/{id}/submit`

- [ ] **Step 1: Write failing integration tests for all REST endpoints**
- [ ] **Step 2: Implement FastAPI routers and register in `main.py` with CORS support**
- [ ] **Step 3: Run pytest across full API suite**
- [ ] **Step 4: Commit changes**

---

### Task 8: Next.js Frontend Scaffolding, Theme & API Client

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/src/app/layout.tsx`
- Create: `frontend/src/app/page.tsx`
- Create: `frontend/src/lib/api-client.ts`
- Create: `frontend/src/components/navbar.tsx`

**Interfaces:**
- Produces: Styled layout with Government of India MoSPI branding, typed API client connecting to FastAPI `http://localhost:8000`

- [ ] **Step 1: Initialize Next.js 14 App Router project with Tailwind CSS and Lucide React**
- [ ] **Step 2: Configure MoSPI Navy/Saffron color theme**
- [ ] **Step 3: Implement `src/lib/api-client.ts` with typed methods for auth, competencies, quizzes, and iGOT**
- [ ] **Step 4: Verify build and linting pass**
- [ ] **Step 5: Commit changes**

---

### Task 9: Officer Portal — Competency Gap Radar Dashboard & iGOT Recommendations

**Files:**
- Create: `frontend/src/app/dashboard/page.tsx`
- Create: `frontend/src/components/competency-radar.tsx`
- Create: `frontend/src/components/gap-summary-cards.tsx`
- Create: `frontend/src/components/igot-course-card.tsx`
- Create: `frontend/src/app/diagnostic/page.tsx`

**Interfaces:**
- Visuals: Interactive Recharts Radar Chart (Current Score vs Target Benchmark), Deficit Cards, iGOT Course Recommendation Cards with Direct Launch Links, Diagnostic Test onboarding

- [ ] **Step 1: Implement `competency-radar.tsx` using Recharts Radar with target vs assessed overlays**
- [ ] **Step 2: Implement `igot-course-card.tsx` with competency level badges, duration, and Karmayogi launch button**
- [ ] **Step 3: Implement `dashboard/page.tsx` connecting live to `/api/competencies/gap-analysis` and `/api/igot/recommendations`**
- [ ] **Step 4: Implement `diagnostic/page.tsx` allowing new officers to take initial 10-question baseline assessment**
- [ ] **Step 5: Verify in browser and commit**

---

### Task 10: Interactive Assessment Player with Direct Document Citations

**Files:**
- Create: `frontend/src/app/assessment/[id]/page.tsx`
- Create: `frontend/src/components/quiz-player.tsx`
- Create: `frontend/src/components/citation-viewer.tsx`

**Interfaces:**
- Visuals: Clean MCQ interface, countdown timer, Bloom's Taxonomy difficulty pill, instant explanation drawer, document page citation accordion

- [ ] **Step 1: Implement `quiz-player.tsx` with question navigation, timer, and radio choice selection**
- [ ] **Step 2: Implement post-submission review displaying correct answer, Bloom's level, technical rationale, and exact document page citations**
- [ ] **Step 3: Implement dynamic toast and score update indicating competency level growth**
- [ ] **Step 4: Commit changes**

---

### Task 11: MoSPI Admin & Trainer Ingestion Studio

**Files:**
- Create: `frontend/src/app/admin/page.tsx`
- Create: `frontend/src/components/document-uploader.tsx`
- Create: `frontend/src/components/question-curator.tsx`
- Create: `frontend/src/components/cadre-analytics.tsx`

**Interfaces:**
- Visuals: Drag-and-drop manual upload (PDF/DOCX), real-time RAG indexing status, Bloom's MCQ generation trigger, question bank curation, cadre gap analytics

- [ ] **Step 1: Implement `document-uploader.tsx` supporting PDF uploads with progress indicator**
- [ ] **Step 2: Implement Bloom's question generator modal triggering `/api/quizzes/generate`**
- [ ] **Step 3: Implement question review and curation cards with live citation inspection**
- [ ] **Step 4: Implement department-wide cadre readiness metrics**
- [ ] **Step 5: Commit changes**

---

### Task 12: Docker Orchestration, Demo Seed Script & End-to-End Verification

**Files:**
- Create: `docker-compose.yml`
- Create: `backend/Dockerfile`
- Create: `frontend/Dockerfile`
- Create: `scripts/demo_setup.sh`
- Create: `README.md`
- Test: `tests/e2e_verification.py`

**Interfaces:**
- Single-command orchestration: `docker-compose up` launches Postgres, FastAPI backend, ChromaDB, and Next.js frontend

- [ ] **Step 1: Write `backend/Dockerfile` and `frontend/Dockerfile`**
- [ ] **Step 2: Write `docker-compose.yml` with health checks and persistent volume mounts**
- [ ] **Step 3: Write comprehensive `demo_setup.sh` that populates sample MoSPI statistical guidelines (PLFS, CPI, National Accounts)**
- [ ] **Step 4: Execute end-to-end integration test verifying complete flow: Ingestion -> Quiz Generation -> Diagnostic -> Radar Chart -> iGOT Recommendations**
- [ ] **Step 5: Update `README.md` with SIH pitch guide and commit**
