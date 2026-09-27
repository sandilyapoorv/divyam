from sqlalchemy.orm import Session
from backend.app.models.competency import CadreRole, Competency, RoleBenchmark
from backend.app.models.user import User, UserCompetencyScore
from backend.app.models.igot import IgotCourse
from backend.app.models.document import Document
from backend.app.models.quiz import Quiz, QuizQuestion

def seed_database(db: Session):
    # Check if already seeded
    if db.query(CadreRole).first():
        return

    # 1. Cadre Roles
    roles_data = [
        {
            "code": "ROLE_STAT_INV_2",
            "title": "Statistical Investigator Grade II",
            "cadre": "Subordinate Statistical Service (SSS)",
            "description": "Frontline official responsible for socio-economic survey execution, CAPI data collection, and preliminary scrutiny in MoSPI FOD."
        },
        {
            "code": "ROLE_ASST_DIR_ISS",
            "title": "Assistant Director / Senior Statistical Officer",
            "cadre": "Indian Statistical Service (ISS)",
            "description": "Technical cadre officer leading survey methodology, National Accounts compilation, and macro-economic index aggregation."
        },
        {
            "code": "ROLE_RES_OFFICER_DES",
            "title": "Research Officer (State DES)",
            "cadre": "State Directorate of Economics & Statistics",
            "description": "State statistical officer overseeing district-level statistical reporting, state GSDP estimations, and local price collections."
        }
    ]

    roles = {}
    for r in roles_data:
        role = CadreRole(**r)
        db.add(role)
        roles[r["code"]] = role
    db.flush()

    # 2. FRAC Competencies
    competencies_data = [
        # Domain
        {
            "code": "COMP_SAMPLING",
            "name": "Survey Sampling & Methodology",
            "type": "Domain",
            "description": "Principles of stratified multi-stage sampling, probability proportional to size (PPS), and sampling error estimation."
        },
        {
            "code": "COMP_NATIONAL_ACCOUNTS",
            "name": "National Accounts Statistics (SNA 2008)",
            "type": "Domain",
            "description": "Gross Value Added (GVA), GDP compilation, supply-use tables, and institutional sector classifications."
        },
        {
            "code": "COMP_PRICE_INDICES",
            "name": "Price & Inflation Indices (CPI / WPI)",
            "type": "Domain",
            "description": "Laspeyres index weighting, basket revision, item price quotation scrutiny, and core inflation calculation."
        },
        {
            "code": "COMP_PLFS_SURVEYS",
            "name": "Periodic Labour Force Survey (PLFS)",
            "type": "Domain",
            "description": "Usual status, current weekly status (CWS), labour force participation rate (LFPR), and urban rotational panel designs."
        },
        # Functional
        {
            "code": "COMP_R_PYTHON_STAT",
            "name": "R / Python for Official Statistics",
            "type": "Functional",
            "description": "Scripting automated data validation, microdata cleaning, dplyr/pandas data wrangling, and reproducible statistical reporting."
        },
        {
            "code": "COMP_CAPI_DATA_VALIDATION",
            "name": "CAPI Field Scrutiny & Data Quality",
            "type": "Functional",
            "description": "Computer Assisted Personal Interviewing validation rules, outlier identification, and logical scrutiny checks."
        },
        # Behavioural
        {
            "code": "COMP_DATA_ETHICS",
            "name": "Data Integrity & Ethical Standards",
            "type": "Behavioural",
            "description": "Adherence to the Collection of Statistics Act, respondent confidentiality, and rigorous prevention of fabricated entries."
        },
        {
            "code": "COMP_ATTENTION_DETAIL",
            "name": "Attention to Granular Detail",
            "type": "Behavioural",
            "description": "Precision in identifying numerical anomalies, cross-table discrepancies, and subtle survey return discrepancies."
        }
    ]

    comps = {}
    for c in competencies_data:
        comp = Competency(**c)
        db.add(comp)
        comps[c["code"]] = comp
    db.flush()

    # 3. Role Benchmarks
    benchmarks_data = [
        # Statistical Investigator Grade II
        ("ROLE_STAT_INV_2", "COMP_SAMPLING", 3, 1.2),
        ("ROLE_STAT_INV_2", "COMP_PLFS_SURVEYS", 4, 1.5),
        ("ROLE_STAT_INV_2", "COMP_CAPI_DATA_VALIDATION", 4, 1.5),
        ("ROLE_STAT_INV_2", "COMP_R_PYTHON_STAT", 2, 0.8),
        ("ROLE_STAT_INV_2", "COMP_PRICE_INDICES", 3, 1.0),
        ("ROLE_STAT_INV_2", "COMP_DATA_ETHICS", 4, 1.2),
        ("ROLE_STAT_INV_2", "COMP_ATTENTION_DETAIL", 4, 1.2),

        # Assistant Director ISS
        ("ROLE_ASST_DIR_ISS", "COMP_SAMPLING", 5, 1.5),
        ("ROLE_ASST_DIR_ISS", "COMP_NATIONAL_ACCOUNTS", 5, 1.5),
        ("ROLE_ASST_DIR_ISS", "COMP_PRICE_INDICES", 4, 1.2),
        ("ROLE_ASST_DIR_ISS", "COMP_PLFS_SURVEYS", 4, 1.2),
        ("ROLE_ASST_DIR_ISS", "COMP_R_PYTHON_STAT", 4, 1.3),
        ("ROLE_ASST_DIR_ISS", "COMP_CAPI_DATA_VALIDATION", 4, 1.0),
        ("ROLE_ASST_DIR_ISS", "COMP_DATA_ETHICS", 5, 1.5),
        ("ROLE_ASST_DIR_ISS", "COMP_ATTENTION_DETAIL", 5, 1.3),
    ]

    for role_code, comp_code, req_level, weight in benchmarks_data:
        bm = RoleBenchmark(
            role_id=roles[role_code].id,
            competency_id=comps[comp_code].id,
            required_level=req_level,
            criticality_weight=weight
        )
        db.add(bm)
    db.flush()

    # 4. Default Seed Users
    # Officer User
    officer = User(
        email="officer.sharma@mospi.gov.in",
        name="Sunil Sharma (SSS)",
        role_id=roles["ROLE_STAT_INV_2"].id,
        department="MoSPI FOD, Regional Office Jaipur",
        is_admin=False
    )
    db.add(officer)

    # Admin User
    admin = User(
        email="admin.director@mospi.gov.in",
        name="Dr. Rajesh Verma (ISS)",
        role_id=roles["ROLE_ASST_DIR_ISS"].id,
        department="National Statistical Systems Training Academy (NSSTA), Greater Noida",
        is_admin=True
    )
    db.add(admin)
    db.flush()

    # Initial Competency Scores for Officer Sharma (Showing realistic baseline gaps)
    officer_scores = [
        ("COMP_SAMPLING", 2.2),             # Target 3 -> Gap 0.8
        ("COMP_PLFS_SURVEYS", 2.5),         # Target 4 -> Gap 1.5 (High Gap!)
        ("COMP_CAPI_DATA_VALIDATION", 3.2), # Target 4 -> Gap 0.8
        ("COMP_R_PYTHON_STAT", 1.0),        # Target 2 -> Gap 1.0
        ("COMP_PRICE_INDICES", 1.5),        # Target 3 -> Gap 1.5 (High Gap!)
        ("COMP_DATA_ETHICS", 3.8),          # Target 4 -> Gap 0.2
        ("COMP_ATTENTION_DETAIL", 3.5),     # Target 4 -> Gap 0.5
    ]

    for comp_code, cur_score in officer_scores:
        score = UserCompetencyScore(
            user_id=officer.id,
            competency_id=comps[comp_code].id,
            current_level=cur_score
        )
        db.add(score)
    db.flush()

    # 5. Authentic iGOT Karmayogi Courses
    igot_courses_data = [
        {
            "igot_id": "IGOT-STAT-001",
            "title": "SNA 2008: Principles of National Accounts Compilation",
            "provider": "NSSTA / MoSPI",
            "description": "Comprehensive self-paced certification on System of National Accounts 2008, GVA estimation, and industry-wise output balancing.",
            "duration_minutes": 720,
            "competency_code": "COMP_NATIONAL_ACCOUNTS",
            "target_level": 4,
            "rating": 4.9,
            "url": "https://karmayogi.gov.in/app/toc/igot_course_sna2008/overview"
        },
        {
            "igot_id": "IGOT-STAT-002",
            "title": "Sample Survey Design & Multi-Stage Sampling Methodologies",
            "provider": "ISI Kolkata / MoSPI",
            "description": "Master stratification, probability proportional to size sampling, sampling frames, and variance estimation for large-scale surveys.",
            "duration_minutes": 480,
            "competency_code": "COMP_SAMPLING",
            "target_level": 3,
            "rating": 4.8,
            "url": "https://karmayogi.gov.in/app/toc/igot_course_sampling_design/overview"
        },
        {
            "igot_id": "IGOT-STAT-003",
            "title": "Periodic Labour Force Survey: Methodology & CWS Estimation",
            "provider": "MoSPI Survey Design & Research Division (SDRD)",
            "description": "Field guide and theoretical foundation for PLFS, rotational sampling in urban strata, and usual status vs weekly status activity.",
            "duration_minutes": 360,
            "competency_code": "COMP_PLFS_SURVEYS",
            "target_level": 4,
            "rating": 4.9,
            "url": "https://karmayogi.gov.in/app/toc/igot_course_plfs_mastery/overview"
        },
        {
            "igot_id": "IGOT-STAT-004",
            "title": "CPI & Inflation: Item Basket Revision & Aggregation",
            "provider": "Karmayogi Bharat / Economic Statistics Division",
            "description": "Learn Laspeyres index methodology, geometric mean aggregation for price relatives, and treatment of missing seasonal price quotations.",
            "duration_minutes": 300,
            "competency_code": "COMP_PRICE_INDICES",
            "target_level": 3,
            "rating": 4.7,
            "url": "https://karmayogi.gov.in/app/toc/igot_course_cpi_inflation/overview"
        },
        {
            "igot_id": "IGOT-STAT-005",
            "title": "CAPI Field Scrutiny & Real-Time Data Quality Assurance",
            "provider": "MoSPI Field Operations Division (FOD)",
            "description": "Best practices for tablet-based interview scrutiny, detecting enumerator interview speed anomalies, and GPS audit logs.",
            "duration_minutes": 240,
            "competency_code": "COMP_CAPI_DATA_VALIDATION",
            "target_level": 3,
            "rating": 4.8,
            "url": "https://karmayogi.gov.in/app/toc/igot_course_capi_scrutiny/overview"
        },
        {
            "igot_id": "IGOT-STAT-006",
            "title": "R Programming for Official Statistical Analysis & Reporting",
            "provider": "NSSTA / Data Quality Assurance Division",
            "description": "Practical hands-on course covering tidyverse, data wrangling for NSS round survey microdata, and automated report generation.",
            "duration_minutes": 540,
            "competency_code": "COMP_R_PYTHON_STAT",
            "target_level": 3,
            "rating": 4.9,
            "url": "https://karmayogi.gov.in/app/toc/igot_course_r_official_stats/overview"
        }
    ]

    for c in igot_courses_data:
        comp_code = c.pop("competency_code")
        course = IgotCourse(
            competency_id=comps[comp_code].id,
            **c
        )
        db.add(course)

    # 6. Sample Initial Manual & Sample Quiz
    sample_doc = Document(
        title="PLFS Instructions to Field Staff 2024",
        filename="PLFS_Field_Instructions_2024.pdf",
        file_path="backend/data/sample_manuals/PLFS_Field_Instructions_2024.pdf",
        total_pages=42,
        status="Indexed"
    )
    db.add(sample_doc)
    db.flush()

    sample_quiz = Quiz(
        title="PLFS Field Survey Scrutiny & Methodology Check",
        document_id=sample_doc.id,
        time_limit_mins=10
    )
    db.add(sample_quiz)
    db.flush()

    # Sample Questions with Citations and Bloom's Levels
    sample_questions = [
        {
            "question": "In the Periodic Labour Force Survey (PLFS), how many times is an urban Sample First Stage Unit (FSU) visited under the rotational panel design?",
            "options": ["1 time only", "2 times across six months", "4 times in consecutive quarters", "8 times over two years"],
            "correct_index": 2,
            "explanation": "In urban areas, a rotational panel sampling design is used where each selected household is visited four times in consecutive quarters (25% rotation scheme).",
            "citation": "PLFS Field Instructions 2024, Page 8, Section 2.3",
            "competency_id": comps["COMP_PLFS_SURVEYS"].id,
            "bloom_level": "Remembering"
        },
        {
            "question": "A member of a surveyed household worked for 2 hours in their family enterprise during the 7 days preceding the survey. Under Current Weekly Status (CWS), how is this individual classified?",
            "options": ["Unemployed", "Out of labour force", "Employed (in labour force)", "Casual wage labourer"],
            "correct_index": 2,
            "explanation": "According to MoSPI standard definitions, a person who had worked for at least 1 hour on any 1 day during the 7 days preceding the date of survey is considered employed under CWS.",
            "citation": "PLFS Field Instructions 2024, Page 16, Section 4.1",
            "competency_id": comps["COMP_PLFS_SURVEYS"].id,
            "bloom_level": "Applying"
        },
        {
            "question": "Why is the Price Relative calculation in MoSPI Consumer Price Index (CPI) performed at the item-stratum level using the Geometric Mean rather than the Arithmetic Mean?",
            "options": [
                "Arithmetic mean produces downward bias",
                "Geometric mean satisfies the time-reversal property and treats proportional price changes symmetrically",
                "Geometric mean is faster to compute on field tablets",
                "To exclude extreme outlier items automatically"
            ],
            "correct_index": 1,
            "explanation": "The Jevons index (Geometric mean of price relatives) satisfies axiomatic properties like time-reversal and treats symmetric proportional changes evenly without upward bias.",
            "citation": "MoSPI Technical Note on CPI Compilation, Page 12, Section 3.1",
            "competency_id": comps["COMP_PRICE_INDICES"].id,
            "bloom_level": "Understanding"
        }
    ]

    for q in sample_questions:
        question = QuizQuestion(
            quiz_id=sample_quiz.id,
            **q
        )
        db.add(question)

    db.commit()
