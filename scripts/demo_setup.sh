#!/usr/bin/env bash
# ==============================================================================
# DIVYAM - Smart India Hackathon (SIH26101) One-Click Demo Setup
# MoSPI Official Statistical Capacity Building & iGOT Karmayogi Platform
# ==============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "======================================================================"
echo "    DIVYAM: Official Statistical System AI Capacity Platform"
echo "    SIH Problem Statement: SIH26101 (MoSPI & Karmayogi Bharat)"
echo "======================================================================"

# Create necessary directories
mkdir -p data/chromadb data/manuals data/uploads

# 1. Check Python virtual environment
if [ -d ".venv" ]; then
    echo "[✓] Found Python virtual environment at .venv"
    PYTHON_EXEC=".venv/bin/python"
    PIP_EXEC=".venv/bin/pip"
else
    echo "[!] Creating Python virtual environment..."
    python3 -m venv .venv
    PYTHON_EXEC=".venv/bin/python"
    PIP_EXEC=".venv/bin/pip"
    $PIP_EXEC install -r backend/requirements.txt
fi

# 2. Run backend test suite to guarantee 100% test integrity
echo "[*] Running Backend Verification Suite (pytest)..."
PYTHONPATH=. $PYTHON_EXEC -m pytest backend/tests/ -v

# 3. Check Node.js and Frontend dependencies
echo "[*] Checking Frontend..."
if [ ! -d "frontend/node_modules" ]; then
    echo "[!] Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

echo ""
echo "======================================================================"
echo " [SUCCESS] DIVYAM is fully prepared for Demonstration!"
echo "======================================================================"
echo ""
echo " To launch the application in development mode:"
echo ""
echo " 1. Start Backend API Server:"
echo "    $ PYTHONPATH=. .venv/bin/uvicorn backend.app.main:app --port 8000 --reload"
echo "    -> OpenAPI Swagger UI: http://localhost:8000/docs"
echo ""
echo " 2. Start Next.js Frontend:"
echo "    $ cd frontend && npm run dev"
echo "    -> Cadre Officer Portal: http://localhost:3000/dashboard"
echo "    -> FRAC Diagnostic:      http://localhost:3000/diagnostic"
echo "    -> Bloom's Quiz Player:  http://localhost:3000/assessment/demo"
echo "    -> MoSPI Admin Studio:   http://localhost:3000/admin"
echo ""
echo " Or launch containerized with Docker Compose:"
echo "    $ docker-compose up --build"
echo "======================================================================"
