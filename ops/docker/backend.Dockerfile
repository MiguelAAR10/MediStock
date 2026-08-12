# syntax=docker/dockerfile:1.6

# ==============================================================================
# MediStock Backend Image
# Used by:
#   - backend service      → python src/clinica_backend/run.py
#   - olap-refresh service → python src/jobs/setup_olap.py / run_olap_cycle.py
# ==============================================================================

ARG PYTHON_VERSION=3.11
ARG REQUIREMENTS_FILE=requirements.txt

FROM python:${PYTHON_VERSION}-slim AS base

# --- System dependencies (psycopg2 needs libpq; build tools for some wheels) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
        ca-certificates \
        tini \
    && rm -rf /var/lib/apt/lists/*

# --- Working directory ---
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    WORKDIR=/app

WORKDIR /app

# --- Layer 1: dependencies (cached unless requirements.txt changes) ---
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# --- Layer 2: source code (rebuilt on code change) ---
COPY src/ /app/src/
COPY notebooks/ /app/notebooks/
COPY ops/ /app/ops/

# --- Streamlit config (used by services that share this image) ---
COPY ops/docker/.streamlit /app/.streamlit

# --- Non-root user for runtime safety ---
RUN groupadd --system medistock && useradd --system --gid medistock medistock \
    && chown -R medistock:medistock /app
USER medistock

# --- Healthcheck (only meaningful for the API service) ---
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:5000/api/health || exit 1

EXPOSE 5000

# --- Tini = proper PID 1 (reaps zombies, signal forwarding) ---
ENTRYPOINT ["/usr/bin/tini", "--"]

# --- Default command (overridden by docker-compose per service) ---
CMD ["python", "src/clinica_backend/run.py"]
