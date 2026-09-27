import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Cover page
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D")) # Deep Navy
        self.drawString(54, letter[1] - 34, "DRIVYAM: Official Statistical Learning & Competency Platform")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawRightString(letter[0] - 54, letter[1] - 34, "SIH26101 | MoSPI & iGOT Karmayogi")
        
        # Header rule
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, letter[1] - 40, letter[0] - 54, letter[1] - 40)
        
        # Footer rule
        self.line(54, 40, letter[0] - 54, 40)
        
        # Footer content
        self.setFont("Helvetica", 8)
        self.drawString(54, 28, "Confidential - Government of India (MoSPI / NIC Meghraj Aligned)")
        self.drawRightString(letter[0] - 54, 28, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def create_flowchart_architecture():
    d = Drawing(504, 115)
    d.add(Rect(0, 0, 504, 115, rx=6, ry=6, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E0"), strokeWidth=1))
    
    # Tier 1: Next.js Frontend
    d.add(Rect(14, 62, 136, 42, rx=5, ry=5, fillColor=colors.HexColor("#2B6CB0"), strokeColor=colors.HexColor("#1A365D"), strokeWidth=1))
    d.add(String(82, 87, "Next.js 14 App Router", fontName="Helvetica-Bold", fontSize=9, fillColor=colors.white, textAnchor="middle"))
    d.add(String(82, 73, "Tailwind + Recharts Radar", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#E2E8F0"), textAnchor="middle"))
    
    # Arrow 1 to 2
    d.add(Line(150, 83, 175, 83, strokeColor=colors.HexColor("#4A5568"), strokeWidth=1.5))
    d.add(Polygon([175, 83, 170, 80, 170, 86], fillColor=colors.HexColor("#4A5568"), strokeColor=None))
    d.add(String(162, 89, "REST", fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor("#4A5568"), textAnchor="middle"))

    # Tier 2: FastAPI Core Engine
    d.add(Rect(180, 12, 154, 94, rx=6, ry=6, fillColor=colors.HexColor("#2C5282"), strokeColor=colors.HexColor("#1A365D"), strokeWidth=1))
    d.add(String(257, 92, "FastAPI Backend Core", fontName="Helvetica-Bold", fontSize=9.5, fillColor=colors.white, textAnchor="middle"))
    
    # Sub-modules inside FastAPI
    d.add(Rect(188, 66, 138, 20, rx=3, ry=3, fillColor=colors.HexColor("#3182CE"), strokeColor=None))
    d.add(String(257, 72, "FRAC Competency Engine", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white, textAnchor="middle"))
    
    d.add(Rect(188, 42, 138, 20, rx=3, ry=3, fillColor=colors.HexColor("#3182CE"), strokeColor=None))
    d.add(String(257, 48, "iGOT Karmayogi Adapter", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white, textAnchor="middle"))
    
    d.add(Rect(188, 18, 138, 20, rx=3, ry=3, fillColor=colors.HexColor("#3182CE"), strokeColor=None))
    d.add(String(257, 24, "RAG Bloom's MCQ Generator", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white, textAnchor="middle"))
    
    # Arrow 2 to 3 (Postgres)
    d.add(Line(334, 76, 356, 76, strokeColor=colors.HexColor("#4A5568"), strokeWidth=1.5))
    d.add(Polygon([356, 76, 351, 73, 351, 79], fillColor=colors.HexColor("#4A5568"), strokeColor=None))
    
    # Arrow 2 to 4 (ChromaDB)
    d.add(Line(334, 30, 356, 30, strokeColor=colors.HexColor("#4A5568"), strokeWidth=1.5))
    d.add(Polygon([356, 30, 351, 27, 351, 33], fillColor=colors.HexColor("#4A5568"), strokeColor=None))

    # Tier 3: PostgreSQL
    d.add(Rect(360, 58, 130, 42, rx=5, ry=5, fillColor=colors.HexColor("#285E61"), strokeColor=colors.HexColor("#1D4044"), strokeWidth=1))
    d.add(String(425, 83, "PostgreSQL Database", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white, textAnchor="middle"))
    d.add(String(425, 69, "Cadre Roles, Scores, Users", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#E6FFFA"), textAnchor="middle"))

    # Tier 4: ChromaDB / Vector Store
    d.add(Rect(360, 12, 130, 40, rx=5, ry=5, fillColor=colors.HexColor("#744210"), strokeColor=colors.HexColor("#502A07"), strokeWidth=1))
    d.add(String(425, 34, "Chroma Vector Store", fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.white, textAnchor="middle"))
    d.add(String(425, 21, "Manuals & Embeddings", fontName="Helvetica", fontSize=7.5, fillColor=colors.HexColor("#FEFCBF"), textAnchor="middle"))

    return d


def create_flowchart_rag():
    d = Drawing(504, 98)
    d.add(Rect(0, 0, 504, 98, rx=6, ry=6, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E0"), strokeWidth=1))
    
    steps = [
        ("MoSPI Manual", "PLFS/CPI/NAS (PDF)", 12, 32, colors.HexColor("#C53030")),
        ("Text Chunking", "1000t Chunk + 200t Ovlp", 112, 32, colors.HexColor("#DD6B20")),
        ("Vector Store", "ChromaDB Embeddings", 212, 32, colors.HexColor("#319795")),
        ("Bloom's Prompt", "Context + FRAC Code", 312, 32, colors.HexColor("#3182CE")),
        ("Verified Quiz", "Options, Rationale, Citation", 410, 32, colors.HexColor("#2F855A"))
    ]
    
    for i, (title, sub, x, y, col) in enumerate(steps):
        d.add(Rect(x, y, 84, 42, rx=5, ry=5, fillColor=col, strokeColor=None))
        d.add(String(x + 42, y + 25, title, fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.white, textAnchor="middle"))
        d.add(String(x + 42, y + 13, sub, fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#EDF2F7"), textAnchor="middle"))
        if i < len(steps) - 1:
            next_x = steps[i+1][2]
            d.add(Line(x + 84, y + 21, next_x, y + 21, strokeColor=colors.HexColor("#718096"), strokeWidth=1.5))
            d.add(Polygon([next_x, y + 21, next_x - 4, y + 18, next_x - 4, y + 24], fillColor=colors.HexColor("#718096"), strokeColor=None))
            
    d.add(String(252, 9, "Hallucination-Free MCQ Generation Pipeline with Direct Page & Section Citations", fontName="Helvetica-Oblique", fontSize=8, fillColor=colors.HexColor("#4A5568"), textAnchor="middle"))
    return d


def create_flowchart_karmayogi():
    d = Drawing(504, 98)
    d.add(Rect(0, 0, 504, 98, rx=6, ry=6, fillColor=colors.HexColor("#F8FAFC"), strokeColor=colors.HexColor("#CBD5E0"), strokeWidth=1))
    
    steps = [
        ("Cadre Role Setup", "Target FRAC L1-L5", 12, 32, colors.HexColor("#2B6CB0")),
        ("Diagnostic Quiz", "Baseline Assessment", 112, 32, colors.HexColor("#4C51BF")),
        ("Gap Radar Engine", "Gap = Max(0, T - C)", 212, 32, colors.HexColor("#D69E2E")),
        ("iGOT Matcher", "Targeted Deficits", 312, 32, colors.HexColor("#38A169")),
        ("Re-Evaluation", "Score Progression", 410, 32, colors.HexColor("#DD6B20"))
    ]
    
    for i, (title, sub, x, y, col) in enumerate(steps):
        d.add(Rect(x, y, 84, 42, rx=5, ry=5, fillColor=col, strokeColor=None))
        d.add(String(x + 42, y + 25, title, fontName="Helvetica-Bold", fontSize=7.2, fillColor=colors.white, textAnchor="middle"))
        d.add(String(x + 42, y + 13, sub, fontName="Helvetica", fontSize=6.5, fillColor=colors.HexColor("#EDF2F7"), textAnchor="middle"))
        if i < len(steps) - 1:
            next_x = steps[i+1][2]
            d.add(Line(x + 84, y + 21, next_x, y + 21, strokeColor=colors.HexColor("#718096"), strokeWidth=1.5))
            d.add(Polygon([next_x, y + 21, next_x - 4, y + 18, next_x - 4, y + 24], fillColor=colors.HexColor("#718096"), strokeColor=None))
            
    d.add(String(252, 9, "Continuous Feedback Loop: Assessment -> Gap Identification -> iGOT Training -> Re-evaluation", fontName="Helvetica-Oblique", fontSize=8, fillColor=colors.HexColor("#4A5568"), textAnchor="middle"))
    return d


def generate_drivyam_pdf(filename="drivyam.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=48
    )
    
    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#1A365D")   # Deep Navy
    secondary_color = colors.HexColor("#2B6CB0") # MoSPI Blue
    accent_color = colors.HexColor("#DD6B20")    # Saffron / Orange
    text_color = colors.HexColor("#2D3748")
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=30,
        leading=36,
        textColor=primary_color,
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=18,
        textColor=secondary_color,
        alignment=1
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        alignment=1
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=text_color,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=text_color
    )
    
    story = []
    
    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 45))
    banner_table = Table(
        [[Paragraph("<b>GOVERNMENT OF INDIA &bull; MINISTRY OF STATISTICS AND PROGRAMME IMPLEMENTATION (MoSPI)</b>", ParagraphStyle('Bnr', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=1))]],
        colWidths=[504]
    )
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 40))
    
    story.append(Paragraph("PROJECT DRIVYAM", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("AI-Enabled Competency Gap Identification, iGOT Karmayogi Personalized Training Recommendation & Bloom's RAG Assessment Platform", subtitle_style))
    story.append(Spacer(1, 24))
    
    badge_data = [
        [
            Paragraph("<b>Problem ID:</b> SIH26101", ParagraphStyle('B1', fontName='Helvetica-Bold', fontSize=9, textColor=primary_color, alignment=1)),
            Paragraph("<b>Domain:</b> Official Statistical System", ParagraphStyle('B2', fontName='Helvetica-Bold', fontSize=9, textColor=secondary_color, alignment=1)),
            Paragraph("<b>Framework:</b> Karmayogi FRAC Model", ParagraphStyle('B3', fontName='Helvetica-Bold', fontSize=9, textColor=accent_color, alignment=1))
        ]
    ]
    badge_table = Table(badge_data, colWidths=[168, 168, 168])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 40))
    
    exec_summary_box = [
        [Paragraph("<b>SYSTEM ARCHITECTURE & CAPABILITY SUMMARY</b>", ParagraphStyle('EbT', fontName='Helvetica-Bold', fontSize=10, textColor=primary_color))],
        [Paragraph(
            "<b>DRIVYAM</b> addresses the critical capacity-building mandate of India's Official Statistical System under MoSPI. "
            "By synthesizing civil service competency modeling (FRAC framework), automated learning path generation via the iGOT Karmayogi ecosystem, "
            "and an advanced Retrieval-Augmented Generation (RAG) assessment engine, the platform enables continuous, verified upskilling for "
            "cadre officers (ISS, SSS, State DES) and grassroots survey investigators across the nation.",
            ParagraphStyle('EbB', fontName='Helvetica', fontSize=9, leading=14, textColor=text_color)
        )]
    ]
    exec_table = Table(exec_summary_box, colWidths=[504])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F4F8")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(exec_table)
    
    story.append(Spacer(1, 80))
    story.append(Paragraph("<b>Comprehensive Technical Design Specification</b><br/>Smart India Hackathon (SIH) &bull; Problem Statement SIH26101<br/>Ministry of Statistics & Programme Implementation (MoSPI) &bull; Karmayogi Bharat Aligned", meta_style))
    story.append(PageBreak())
    
    # ================= PAGE 2: PROBLEM STATEMENT & CORE PILLARS =================
    story.append(Paragraph("1. Executive Problem Statement & Context", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "India's Official Statistical System, stewarded by the Ministry of Statistics and Programme Implementation (MoSPI), "
        "relies heavily on specialized technical cadres: the <b>Indian Statistical Service (ISS)</b>, the <b>Subordinate Statistical Service (SSS)</b>, "
        "State Directorates of Economics & Statistics (DES), and field enumerators in the Field Operations Division (FOD). "
        "These personnel compile vital sovereign indicators such as Gross Value Added (GVA), Consumer Price Index (CPI), Wholesale Price Index (WPI), "
        "Index of Industrial Production (IIP), and Periodic Labour Force Surveys (PLFS).",
        body_style
    ))
    story.append(Paragraph(
        "Despite extensive publication of manuals and methodologies, existing training faces <b>three acute bottlenecks</b>: "
        "(1) <i>Untracked Competency Deficits</i> — no automated mechanism to identify where an individual officer lacks proficiency relative to their cadre benchmark; "
        "(2) <i>Fragmented Upskilling</i> — lack of dynamic routing to relevant learning modules on the National iGOT Karmayogi Bharat portal; "
        "(3) <i>Passive Document Ingestion</i> — departmental training manuals remain static PDFs rather than interactive, verifiable knowledge checkpoints.",
        body_style
    ))
    story.append(Spacer(1, 8))
    
    pillar_data = [
        [
            Paragraph("<b>Pillar 1: FRAC Competency Engine</b>", table_header_style),
            Paragraph("<b>Pillar 2: iGOT Karmayogi Adapter</b>", table_header_style),
            Paragraph("<b>Pillar 3: Bloom's RAG Quiz Engine</b>", table_header_style)
        ],
        [
            Paragraph("Implements the official GoI FRAC model (Roles, Activities, Competencies across Domain, Functional, and Behavioural axes). Evaluates baseline via diagnostic tests and renders dynamic Radar Gap charts.", table_cell_style),
            Paragraph("Calculates competency deficits and recommends targeted iGOT courses. Implements a standards-compliant adapter pre-seeded with authentic MoSPI modules, ready for live API integration.", table_cell_style),
            Paragraph("Ingests official manuals (PDF/DOCX), generates multi-tier MCQs (Remembering, Understanding, Applying, Analyzing) with strict page/section citations and zero hallucination.", table_cell_style)
        ]
    ]
    pillar_table = Table(pillar_data, colWidths=[168, 168, 168])
    pillar_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(pillar_table)
    story.append(Spacer(1, 14))
    
    # Key Persona Box
    persona_box = [
        [Paragraph("<b>CORE PLATFORM PERSONAS & VALUE PROPOSITION</b>", ParagraphStyle('PbT', fontName='Helvetica-Bold', fontSize=9, textColor=primary_color))],
        [Paragraph(
            "<b>1. Statistical Officers (Learners):</b> Onboard by cadre role &rarr; Complete diagnostic test &rarr; View interactive Competency Radar Chart &rarr; Launch personalized iGOT Karmayogi courses &rarr; Take practice quizzes with citations.<br/>"
            "<b>2. MoSPI / NSSTA Trainers (Admins):</b> Upload official statistical manuals &rarr; Trigger Bloom's-level MCQ generation &rarr; Curate question banks &rarr; Monitor cadre-wide competency distributions across states.",
            ParagraphStyle('PbB', fontName='Helvetica', fontSize=8.5, leading=13, textColor=text_color)
        )]
    ]
    persona_table = Table(persona_box, colWidths=[504])
    persona_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(persona_table)
    story.append(PageBreak())

    # ================= PAGE 3: SYSTEM ARCHITECTURE =================
    story.append(Paragraph("2. System Architecture & High-Level Flowchart", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "DRIVYAM is engineered as a production-grade, modular full-stack platform. The architecture separates presentation logic "
        "(Next.js 14 App Router) from high-throughput AI and competency analytics (FastAPI asynchronous micro-services), backed by "
        "PostgreSQL for relational integrity and ChromaDB for vector retrieval.",
        body_style
    ))
    
    story.append(create_flowchart_architecture())
    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>Figure 1: High-level System Architecture of DRIVYAM showing interaction between Presentation, Core Engine, and Persistence layers.</i>", ParagraphStyle('FigC', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#718096"), alignment=1)))
    story.append(Spacer(1, 8))
    
    tech_data = [
        [Paragraph("<b>Component Layer</b>", table_header_style), Paragraph("<b>Technology Selection</b>", table_header_style), Paragraph("<b>Architectural Justification & Role</b>", table_header_style)],
        [Paragraph("<b>Frontend Client</b>", table_cell_style), Paragraph("Next.js 14, React 18, Tailwind CSS, Lucide Icons, Recharts", table_cell_style), Paragraph("Responsive, role-differentiated portals for Statistical Officers and Admins. Dynamic multi-axis Radar Gap charts.", table_cell_style)],
        [Paragraph("<b>Application Server</b>", table_cell_style), Paragraph("Python 3.11+ FastAPI, Pydantic v2, SQLAlchemy 2.0", table_cell_style), Paragraph("Asynchronous REST API with high performance, automated Swagger docs, and native Python AI ecosystem interoperability.", table_cell_style)],
        [Paragraph("<b>Relational DB</b>", table_cell_style), Paragraph("PostgreSQL (Dockerized / Meghraj Cloud)", table_cell_style), Paragraph("Stores official cadre roles, user profiles, competency benchmarks, quiz attempts, and iGOT course catalogs.", table_cell_style)],
        [Paragraph("<b>Vector Store</b>", table_cell_style), Paragraph("ChromaDB / Pinecone / Weaviate", table_cell_style), Paragraph("Persists semantic embeddings of chunked MoSPI manuals with page numbers and section IDs for RAG.", table_cell_style)],
        [Paragraph("<b>AI / LLM Layer</b>", table_cell_style), Paragraph("LangChain RAG + HuggingFace / Llama 3 / Gemini", table_cell_style), Paragraph("Extracts statistical entities, maps concepts to FRAC taxonomy, and synthesizes Bloom's-rated assessment questions.", table_cell_style)],
        [Paragraph("<b>Cloud / Infra</b>", table_cell_style), Paragraph("Docker Compose, Kubernetes, NIC Meghraj Cloud Ready", table_cell_style), Paragraph("Adheres to GoI cloud hosting mandates: stateless containers, environment secret injection, and horizontal scalability.", table_cell_style)]
    ]
    tech_table = Table(tech_data, colWidths=[95, 155, 254])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(tech_table)
    story.append(PageBreak())

    # ================= PAGE 4: FRAC FRAMEWORK & IGOT INTEGRATION =================
    story.append(Paragraph("3. FRAC Framework & iGOT Karmayogi Ecosystem Integration", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "Karmayogi Bharat establishes the <b>FRAC model</b> (Framework for Roles, Activities, and Competencies) to transition civil service "
        "human resource management from 'rules-based' to 'roles-based'. DRIVYAM adopts this exact ontology specifically calibrated for "
        "India's statistical cadre hierarchy.",
        body_style
    ))
    
    story.append(create_flowchart_karmayogi())
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>Figure 2: The DRIVYAM Competency Lifecycle and iGOT Karmayogi Closed-Loop Learning Progression.</i>", ParagraphStyle('FigC2', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#718096"), alignment=1)))
    story.append(Spacer(1, 6))

    story.append(Paragraph("FRAC Competency Classification in Official Statistics", h2_style))
    
    frac_data = [
        [Paragraph("<b>Competency Category</b>", table_header_style), Paragraph("<b>Key MoSPI Competencies</b>", table_header_style), Paragraph("<b>Proficiency Scale (Levels 1 to 5)</b>", table_header_style)],
        [
            Paragraph("<b>Domain Competencies</b><br/>(Technical Statistical Knowledge)", table_cell_style),
            Paragraph("&bull; Survey Sampling & Design<br/>&bull; National Accounts (SNA 2008)<br/>&bull; Price Indices (CPI / WPI)<br/>&bull; Index of Industrial Production (IIP)<br/>&bull; Periodic Labour Force Survey (PLFS)", table_cell_style),
            Paragraph("<b>Level 1:</b> Awareness of terminology<br/><b>Level 2:</b> Basic field execution<br/><b>Level 3:</b> Autonomous data compilation<br/><b>Level 4:</b> Methodology auditing & design<br/><b>Level 5:</b> Policy & framework authoring", table_cell_style)
        ],
        [
            Paragraph("<b>Functional Competencies</b><br/>(Execution & Technology)", table_cell_style),
            Paragraph("&bull; R/Python for Official Statistics<br/>&bull; CAPI/Tablet Field Data Validation<br/>&bull; Microdata Scrutiny & Imputation<br/>&bull; Survey Team Supervision", table_cell_style),
            Paragraph("<b>Level 1:</b> Basic data entry/viewing<br/><b>Level 2:</b> Routine scripting & execution<br/><b>Level 3:</b> Complex validation rules<br/><b>Level 4:</b> Pipeline architecture & QC<br/><b>Level 5:</b> Enterprise data governance", table_cell_style)
        ],
        [
            Paragraph("<b>Behavioural Competencies</b><br/>(Public Service Values)", table_cell_style),
            Paragraph("&bull; Data Integrity & Ethical Conduct<br/>&bull; Attention to Granular Detail<br/>&bull; Cross-Cadre Collaboration", table_cell_style),
            Paragraph("<b>Level 1:</b> Adherence to protocol<br/><b>Level 2:</b> Proactive discrepancy reporting<br/><b>Level 3:</b> Quality culture leadership", table_cell_style)
        ]
    ]
    frac_table = Table(frac_data, colWidths=[125, 185, 194])
    frac_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(frac_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Competency Gap Formula & Radar Visualization", h2_style))
    story.append(Paragraph(
        "For an officer <i>u</i> holding cadre role <i>r</i>, competency gap for competency <i>c</i> is computed as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Gap<sub>c</sub> = max(0, TargetLevel<sub>r,c</sub> - CurrentScore<sub>u,c</sub>)</b><br/>"
        "Overall <b>Cadre Readiness Index (&Omega;)</b> is computed using role importance weights <i>w<sub>c</sub></i>: "
        "<b>&Omega; = &Sigma; [ w<sub>c</sub> &times; min(1.0, CurrentScore<sub>u,c</sub> / TargetLevel<sub>r,c</sub>) ]</b>. "
        "Gaps are plotted on a dynamic multi-axis radar chart, instantly driving personalized course recommendations.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Sample iGOT Karmayogi Course Recommendation Catalog", h2_style))
    igot_sample_data = [
        [Paragraph("<b>Course ID</b>", table_header_style), Paragraph("<b>Course Title</b>", table_header_style), Paragraph("<b>Provider</b>", table_header_style), Paragraph("<b>Target Competency</b>", table_header_style), Paragraph("<b>Duration</b>", table_header_style)],
        [Paragraph("IGOT-STAT-001", table_cell_style), Paragraph("SNA 2008: Principles of National Accounts", table_cell_style), Paragraph("NSSTA / MoSPI", table_cell_style), Paragraph("National Accounts (L3)", table_cell_style), Paragraph("12 hrs (Self-paced)", table_cell_style)],
        [Paragraph("IGOT-STAT-002", table_cell_style), Paragraph("Sample Survey Design & Multi-Stage Sampling", table_cell_style), Paragraph("ISI Kolkata / MoSPI", table_cell_style), Paragraph("Survey Sampling (L3)", table_cell_style), Paragraph("8 hrs", table_cell_style)],
        [Paragraph("IGOT-STAT-003", table_cell_style), Paragraph("CPI & Inflation: Basket Revision & Indexing", table_cell_style), Paragraph("Karmayogi Bharat", table_cell_style), Paragraph("Price Indices (L2)", table_cell_style), Paragraph("6 hrs", table_cell_style)],
        [Paragraph("IGOT-STAT-004", table_cell_style), Paragraph("Data Quality & CAPI Field Scrutiny", table_cell_style), Paragraph("MoSPI FOD", table_cell_style), Paragraph("Data Validation (L3)", table_cell_style), Paragraph("4 hrs", table_cell_style)]
    ]
    igot_sample_table = Table(igot_sample_data, colWidths=[80, 174, 90, 100, 60])
    igot_sample_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#285E61")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(igot_sample_table)
    story.append(PageBreak())

    # ================= PAGE 5: RAG ASSESSMENT GENERATOR =================
    story.append(Paragraph("4. RAG-Powered Assessment & Bloom's Taxonomy Quiz Generator", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=8))
    
    story.append(Paragraph(
        "A cornerstone of DRIVYAM is transforming extensive government manuals (e.g. 200-page PLFS Instructions to Field Staff) "
        "into verifiable, pedagogically structured learning checkpoints. The pipeline prevents AI hallucinations by binding every question "
        "to explicit document coordinates.",
        body_style
    ))
    
    story.append(create_flowchart_rag())
    story.append(Spacer(1, 4))
    story.append(Paragraph("<i>Figure 3: Retrieval-Augmented Generation (RAG) Architecture for Bloom's Taxonomy Assessment Creation.</i>", ParagraphStyle('FigC3', fontName='Helvetica-Oblique', fontSize=7.5, textColor=colors.HexColor("#718096"), alignment=1)))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Bloom's Revised Taxonomy Question Hierarchy", h2_style))
    
    bloom_data = [
        [Paragraph("<b>Bloom Level</b>", table_header_style), Paragraph("<b>Cognitive Focus in Statistics</b>", table_header_style), Paragraph("<b>Illustrative MCQ Scenario</b>", table_header_style)],
        [
            Paragraph("<b>Level 1: Remembering</b>", table_cell_style),
            Paragraph("Factual recall of definitions, base years, and formulas.", table_cell_style),
            Paragraph("<i>What is the current base year utilized by MoSPI for compiling the All-India Consumer Price Index (CPI-Rural/Urban)?</i><br/>(Options: 2004-05, 2011-12, 2017-18, 2020-21)", table_cell_style)
        ],
        [
            Paragraph("<b>Level 2: Understanding</b>", table_cell_style),
            Paragraph("Comprehending methodology rationale and concepts.", table_cell_style),
            Paragraph("<i>Why does the Periodic Labour Force Survey (PLFS) employ a rotational panel sampling design in urban areas rather than independent cross-sections?</i>", table_cell_style)
        ],
        [
            Paragraph("<b>Level 3: Applying</b>", table_cell_style),
            Paragraph("Executing procedures in concrete field survey situations.", table_cell_style),
            Paragraph("<i>A field investigator encounters a multi-household dwelling where the primary earner has temporarily migrated for 4 months. How should the household status be classified under Schedule 10.4?</i>", table_cell_style)
        ],
        [
            Paragraph("<b>Level 4: Analyzing</b>", table_cell_style),
            Paragraph("Dissecting data inconsistencies and audit discrepancies.", table_cell_style),
            Paragraph("<i>Given a mismatch between ASI factory return gross output and enterprise balance sheet turnover, identify the primary imputation error source according to MoSPI scrutiny protocols.</i>", table_cell_style)
        ]
    ]
    bloom_table = Table(bloom_data, colWidths=[110, 155, 239])
    bloom_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2F855A")),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(bloom_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Hallucination Prevention & Citation Verification Protocol", h2_style))
    story.append(Paragraph(
        "To guarantee 100% fidelity to official government manuals, DRIVYAM enforces a <b>strict citation contract</b>. "
        "During generation, the LLM is constrained by system prompts requiring JSON output adhering to: "
        "<code>{\"citation\": {\"document\": string, \"page\": int, \"section\": string, \"verbatim_excerpt\": string}}</code>. "
        "Any question lacking an exact excerpt match in the retrieved chunk is discarded during automated validation.",
        body_style
    ))
    story.append(PageBreak())

    # ================= PAGE 6: DATABASE SCHEMA, CLOUD DEPLOYMENT & EVALUATION =================
    story.append(Paragraph("5. Technical Blueprint, Security & Meghraj Cloud Deployment", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=6))
    
    db_schema_data = [
        [Paragraph("<b>Table Entity</b>", table_header_style), Paragraph("<b>Primary Fields & Types</b>", table_header_style), Paragraph("<b>Relational Purpose</b>", table_header_style)],
        [Paragraph("<code>users</code>", table_cell_style), Paragraph("id (UUID), email, full_name, role_id, cadre, is_admin", table_cell_style), Paragraph("User authentication, cadre association (ISS/SSS/DES).", table_cell_style)],
        [Paragraph("<code>cadre_roles</code>", table_cell_style), Paragraph("id, code, title, cadre_category, min_experience_years", table_cell_style), Paragraph("MoSPI cadre designation benchmark master.", table_cell_style)],
        [Paragraph("<code>competencies</code>", table_cell_style), Paragraph("id, code, title, category (Domain/Func/Beh), description", table_cell_style), Paragraph("Official FRAC competency ontology master.", table_cell_style)],
        [Paragraph("<code>role_benchmarks</code>", table_cell_style), Paragraph("role_id (FK), competency_id (FK), target_level (1-5), weight", table_cell_style), Paragraph("Target competency standard matrix per role.", table_cell_style)],
        [Paragraph("<code>user_scores</code>", table_cell_style), Paragraph("user_id (FK), competency_id (FK), current_score (Float), updated_at", table_cell_style), Paragraph("Live calculated competency levels feeding Radar Chart.", table_cell_style)],
        [Paragraph("<code>documents</code>", table_cell_style), Paragraph("id, title, file_path, doc_hash, total_pages, status", table_cell_style), Paragraph("Uploaded MoSPI training manual metadata.", table_cell_style)],
        [Paragraph("<code>quizzes</code>", table_cell_style), Paragraph("id, title, doc_id (FK), total_marks, pass_percent, time_limit", table_cell_style), Paragraph("Assessment containers generated via RAG.", table_cell_style)],
        [Paragraph("<code>quiz_questions</code>", table_cell_style), Paragraph("id, quiz_id (FK), question, options (JSON), correct_idx, citation, bloom", table_cell_style), Paragraph("Granular MCQs tagged with FRAC code & page citation.", table_cell_style)]
    ]
    db_table = Table(db_schema_data, colWidths=[90, 210, 204])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(db_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("6. Hackathon Evaluation Alignment (SIH26101 Criteria)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=6))
    
    eval_data = [
        [Paragraph("<b>Evaluation Criterion</b>", table_header_style), Paragraph("<b>SIH Expectation</b>", table_header_style), Paragraph("<b>How DRIVYAM Exceeds Expectations</b>", table_header_style)],
        [
            Paragraph("<b>Innovation & AI Depth</b>", table_cell_style),
            Paragraph("Meaningful use of Generative AI beyond generic chat.", table_cell_style),
            Paragraph("Full RAG pipeline with Bloom's Revised Taxonomy question generation, auto-citation extraction, and FRAC competency tagging.", table_cell_style)
        ],
        [
            Paragraph("<b>Government Alignment</b>", table_cell_style),
            Paragraph("True fit for MoSPI & Karmayogi ecosystem.", table_cell_style),
            Paragraph("Adheres strictly to DoPT/Karmayogi Bharat FRAC ontology and course schemas, seeded with authentic MoSPI cadre data (ISS/SSS).", table_cell_style)
        ],
        [
            Paragraph("<b>Viability & Completeness</b>", table_cell_style),
            Paragraph("Working prototype with low friction.", table_cell_style),
            Paragraph("Complete end-to-end integration: Document Upload -> AI Quiz Generator -> Interactive Test -> Dynamic Gap Radar -> iGOT Course Launch.", table_cell_style)
        ],
        [
            Paragraph("<b>Security & Scalability</b>", table_cell_style),
            Paragraph("Readiness for government cloud deployment.", table_cell_style),
            Paragraph("Dockerized, stateless microservices aligned with NIC Meghraj Cloud and Cert-In security guidelines.", table_cell_style)
        ]
    ]
    eval_table = Table(eval_data, colWidths=[105, 145, 254])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary_color),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(eval_table)
    story.append(Spacer(1, 8))

    closing_box = [
        [Paragraph("<b>CONFIRMATION & DEPLOYMENT SIGN-OFF</b>", ParagraphStyle('CbT', fontName='Helvetica-Bold', fontSize=8.5, textColor=primary_color))],
        [Paragraph(
            "<b>DRIVYAM: Official Statistical Learning & Competency Platform</b> is primed for live execution and staging. "
            "All functional flows, schemas, data contracts, and presentation designs are validated and synchronized across project memory.",
            ParagraphStyle('CbB', fontName='Helvetica', fontSize=8, leading=12, textColor=text_color)
        )]
    ]
    closing_table = Table(closing_box, colWidths=[504])
    closing_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#90CDF4")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(closing_table)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    generate_drivyam_pdf("drivyam.pdf")
