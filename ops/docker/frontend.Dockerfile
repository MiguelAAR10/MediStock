# syntax=docker/dockerfile:1.6

# ==============================================================================
# MediStock Frontend Image (Streamlit)
# Serves the multipage UI on port 8501.
# ==============================================================================

ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    STREAMLIT_CONFIG_DIR=/app/.streamlit \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# --- System deps ---
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        tini \
    && rm -rf /var/lib/apt/lists/*

# --- Layer 1: frontend-only dependencies ---
COPY src/clinica_frontend/requirements.txt /app/requirements-frontend.txt
RUN pip install --upgrade pip && pip install -r /app/requirements-frontend.txt

# --- Layer 2: frontend code ---
COPY src/clinica_frontend/ /app/src/clinica_frontend/

# --- Streamlit config (port, address, disable telemetry) ---
COPY ops/docker/.streamlit /app/.streamlit

# --- Non-root runtime user ---
RUN groupadd --system medistock && useradd --system --gid medistock medistock \
    && chown -R medistock:medistock /app
USER medistock

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]

# Streamlit is launched from src/clinica_frontend/ so its relative imports work.
CMD ["streamlit", "run", "src/clinica_frontend/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
