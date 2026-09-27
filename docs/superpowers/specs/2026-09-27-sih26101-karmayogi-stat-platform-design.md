# Design Specification: AI-Enabled Learning Platform for India's Official Statistical System (SIH26101)

- **Date**: 2026-09-27
- **Problem Statement ID**: SIH26101
- **Target Cadres**: Indian Statistical Service (ISS), Subordinate Statistical Service (SSS), State Directorates of Economics & Statistics (DES), and MoSPI Field Enumerators
- **Status**: Ready for Implementation Planning

---

## 1. Executive Summary & Objective

The objective of this platform is to build an AI-powered competency profiling, learning recommendation, and assessment system tailored for India's Official Statistical System under the Ministry of Statistics and Programme Implementation (MoSPI). The platform:
1. **Identifies Competency Gaps**: Uses the Government of India's **FRAC framework** (Framework for Roles, Activities, and Competencies) to benchmark officers against role standards across Domain, Functional, and Behavioural axes (Levels 1 to 5).
2. **Recommends Personalized Training via iGOT Karmayogi**: Maps identified skill deficits directly to curated, official iGOT Karmayogi courses and learning pathways using a standards-compliant adapter.
3. **Generates Quizzes & Assessments from Ingested Materials**: Ingests official MoSPI statistical manuals, survey guidelines, and methodology papers (PDF/DOCX) to produce verified MCQs tagged with **Bloom's Taxonomy** levels, FRAC competencies, and **exact document citations**.

---

## 2. Target Personas & Core User Journeys

### Persona A: Statistical Officer / Cadre Learner (e.g. Statistical Investigator Grade II, Assistant Director)
1. **Onboarding & Role Benchmarking**: Selects official cadre/role in MoSPI (e.g., *Survey Sampling & Methodology*, *National Accounts Division*, *Price & Inflation Statistics*). The platform loads the target FRAC competency profile.
2. **Diagnostic Baseline Assessment**: Completes a structured 10-question diagnostic test to establish their baseline competency levels.
3. **Competency Gap Radar Dashboard**: Visualizes current competency levels vs. benchmark requirements on an interactive Radar/Spider chart. Identifies critical gap areas.
4. **iGOT Karmayogi Learning Pathway**: Reviews prioritized course recommendations with course metadata, estimated duration, competency level progression, and direct launch links.
5. **Continuous Assessment & Upskilling**: Takes chapter quizzes generated from newly uploaded departmental guidelines. Successful quiz completion dynamically updates their competency profile in real time.

### Persona B: MoSPI Trainer / Departmental Administrator (e.g. Director of Training at NASA - National Statistical Systems Training Academy)
1. **Curriculum & Manual Ingestion**: Uploads official documents (e.g., *PLFS Annual Survey Manual*, *CPI Technical Note*, *System of National Accounts Handbook*).
2. **AI Question Bank Generation**: Configures target question parameters (number of questions, Bloom's difficulty tiers) and generates verified MCQs.
3. **Question Review & Curating**: Edits, approves, or rejects generated questions with live preview of source document citations.
4. **Cadre Readiness Analytics**: Monitors department-wide competency distributions, identifies systemic skill gaps across divisions, and exports reports.

---

## 3. System Architecture & Tech Stack

```
+-----------------------------------------------------------------------------------+
|                            Next.js 14+ Frontend (SPA)                             |
|  - Tailwind CSS + Lucide Icons + Recharts (Dynamic Competency Radar & Gap Charts)  |
|  - Role-based Layouts: Officer Dashboard, Quiz Player, Admin Ingestion Studio     |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST (JSON)
                                           v
+-----------------------------------------------------------------------------------+
|                            FastAPI Modular Backend (Python)                       |
|  +--------------------+  +----------------------+  +----------------------------+ |
|  | Auth & Cadre Roles |  | FRAC Competency Core |  |  iGOT Karmayogi Adapter    | |
|  +--------------------+  +----------------------+  +----------------------------+ |
|  +--------------------+  +----------------------+  +----------------------------+ |
|  | Document Ingestion |  | LangChain RAG Engine |  |  Bloom's MCQ Generator    | |
|  +--------------------+  +----------------------+  +----------------------------+ |
+---------------------+-------------------------------+-----------------------------+
                      |                               |
                      v                               v
+-----------------------------------+   +-------------------------------------------+
|      PostgreSQL Database          |   |          ChromaDB / Vector Store          |
|  - Users, Roles, Assessments      |   |  - Chunked MoSPI Manuals & Methodology    |
|  - FRAC Matrix & Competency Scores|   |  - Statistical Concept Embeddings         |
+-----------------------------------+   +-------------------------------------------+
```

### Technology Matrix
* **Frontend**: Next.js 14 (App Router), React 18, Tailwind CSS, Lucide React, Recharts
* **Backend API**: Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0 (Async/Sync)
* **Database**: PostgreSQL (Structured data), ChromaDB (Vector store for document chunks)
* **AI / NLP**: LangChain, HuggingFace embeddings (`all-MiniLM-L6-v2`), Gemini API / Llama 3 via LangChain for generation, PyPDF/pdfplumber for extraction
* **Deployment**: Docker, `docker-compose.yml`, Kubernetes deployment manifests aligned with NIC Meghraj Cloud guidelines

---

## 4. Detailed Component Specifications

### 4.1. FRAC Competency Engine
* Implements the official Karmayogi Bharat FRAC model:
  * **Role**: e.g., "Statistical Investigator (Field Survey)", "Assistant Director (National Accounts)"
  * **Activity**: e.g., "Stratified Multistage Sampling", "GVA Computation", "Index Compilation"
  * **Competency**:
    * **Domain**: *Survey Sampling Theory*, *National Accounts Methodology*, *CPI/WPI Price Aggregation*, *Data Quality Auditing*
    * **Functional**: *Field Team Supervision*, *R/Python Statistical Computing*, *Data Validation Protocols*
    * **Behavioural**: *Attention to Detail*, *Ethical Data Handling*, *Problem Solving*
  * **Levels**: 1 (Awareness), 2 (Basic), 3 (Competent), 4 (Advanced), 5 (Expert)
* **Gap Calculation Algorithm**:
  $$\text{Gap}_c = \max(0, \text{TargetLevel}_{r, c} - \text{CurrentLevel}_{u, c})$$
  Priority weight is computed based on role criticality score.

### 4.2. iGOT Karmayogi Adapter Service
* Pluggable client architecture (`IgotClient`):
  * **Sandbox Mode**: Pre-seeded with 15+ authentic MoSPI-tailored iGOT courses matching the official Karmayogi metadata schema (Course ID, Title, Provider, Competency Mappings with Target Level, Duration, Rating, Direct Deep Link).
  * **Live API Mode**: Configurable via `IGOT_API_BASE_URL` and `IGOT_API_KEY` environment variables.
* **Course Matching Logic**:
  * Scans user's top competency gaps ($\text{Gap}_c > 0$).
  * Filters iGOT catalog where `course.competency_id == gap.competency_id` and `course.level >= user.current_level`.
  * Ranks by gap severity and course rating.

### 4.3. RAG-Powered Assessment & Quiz Generation Engine
* **Document Parser**: Handles multi-page PDFs and text files, extracting clean text while preserving section/chapter metadata and page numbers.
* **Chunking**: RecursiveCharacterTextSplitter (chunk size: 1000 tokens, overlap: 200 tokens) retaining source metadata (`{"source_file": "...", "page": 14, "section": "3.2"}`).
* **Vector Store**: ChromaDB instance storing document embeddings.
* **Bloom's Taxonomy Generation Pipeline**:
  * Prompts the LLM with retrieved context chunks.
  * Generates 4-option MCQs categorized into:
    * **Level 1 (Remembering/Understanding)**: Factual definitions, index formulas, MoSPI classification standards.
    * **Level 2 (Applying)**: Scenario-based problem solving (e.g., choosing correct sampling method given village population skew).
    * **Level 3 (Analyzing/Evaluating)**: Identifying data discrepancies in survey returns or national accounts reconciliations.
  * Each question MUST include:
    * `question`: String
    * `options`: Array of 4 strings
    * `correct_index`: 0 to 3
    * `explanation`: Detailed technical reasoning
    * `citation`: Document name, chapter, and page reference
    * `competency_id`: Mapped FRAC competency code
    * `bloom_level`: "Remembering" | "Understanding" | "Applying" | "Analyzing"

---

## 5. Database Schema & Data Models

### Key Entities
1. **User**: `id`, `name`, `email`, `role_id` (foreign key to CadreRole), `department` (e.g. "FOD Kolkata", "NAD Delhi"), `is_admin`
2. **CadreRole**: `id`, `code` (e.g. "ROLE_STAT_INV_2"), `title`, `description`, `cadre` ("ISS" / "SSS" / "State DES")
3. **Competency**: `id`, `code` (e.g. "COMP_SAMPLING"), `name`, `type` ("Domain", "Functional", "Behavioural"), `description`
4. **RoleCompetencyBenchmark**: `role_id`, `competency_id`, `required_level` (1-5)
5. **UserCompetencyScore**: `user_id`, `competency_id`, `current_level` (1.0-5.0 float), `last_assessed_at`
6. **IgotCourse**: `id`, `igot_id`, `title`, `provider` (e.g. "NSSTA", "Karmayogi Bharat"), `description`, `duration_minutes`, `competency_id`, `target_level`, `url`, `thumbnail_url`
7. **Document**: `id`, `title`, `file_path`, `file_type`, `uploaded_by`, `uploaded_at`, `status` ("Indexed", "Processing")
8. **Quiz**: `id`, `title`, `document_id`, `created_by`, `created_at`, `time_limit_mins`
9. **QuizQuestion**: `id`, `quiz_id`, `question`, `options` (JSON), `correct_index`, `explanation`, `citation`, `competency_id`, `bloom_level`
10. **QuizAttempt**: `id`, `user_id`, `quiz_id`, `score`, `total_questions`, `answers` (JSON), `completed_at`

---

## 6. API Endpoints Specification

### Authentication & Profiles
* `POST /api/auth/login`: Mock/JWT login supporting Officer and Trainer logins.
* `GET /api/auth/me`: Current user profile, role, and department.

### Competency & iGOT Recommendations
* `GET /api/competencies/roles`: List all available MoSPI/State DES roles.
* `GET /api/competencies/gap-analysis`: Returns user's radar chart data (required vs current scores across competencies) and calculated gaps.
* `POST /api/competencies/initialize-diagnostic`: Initializes or updates scores from a diagnostic test.
* `GET /api/igot/recommendations`: Returns personalized iGOT Karmayogi courses prioritized by the officer's highest competency deficits.
* `GET /api/igot/catalog`: Returns browsable iGOT catalog with filtering by competency type.

### Ingestion & Quizzes
* `POST /api/documents/upload`: Upload PDF/DOCX statistical manual and trigger background/immediate vector indexing.
* `GET /api/documents`: List uploaded MoSPI documents.
* `POST /api/quizzes/generate`: Trigger AI generation of Bloom's taxonomy MCQs from a document.
* `GET /api/quizzes`: List available quizzes.
* `GET /api/quizzes/{id}`: Fetch quiz questions (without answers for active player, with answers for admin review).
* `POST /api/quizzes/{id}/submit`: Submit quiz answers, get instant grading, review explanations/citations, and trigger automatic FRAC competency score updates.

---

## 7. Verification & Testing Strategy

1. **Backend Unit & Integration Tests**:
   * Test FRAC gap calculation logic with boundary conditions (scores 1 to 5).
   * Test iGOT recommendation algorithm matching accuracy.
   * Test PDF text extraction, chunking, and ChromaDB vector retrieval.
   * Test quiz grading and competency update mutations.
2. **Frontend End-to-End Verification**:
   * Officer Login $\rightarrow$ Role selection $\rightarrow$ Diagnostic quiz $\rightarrow$ Radar Chart rendering verification.
   * iGOT course recommendation display and deep-linking verification.
   * Trainer document upload $\rightarrow$ MCQ generation with citations and Bloom's taxonomy verification.
3. **Deployment Smoke Test**:
   * Verify all services start and run cleanly via `docker-compose up`.
