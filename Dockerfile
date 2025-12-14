FROM python:3.10-slim

# ============================================================
# System dependencies
# ============================================================
RUN apt-get update && \
    apt-get install -y git wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ============================================================
# Workdir
# ============================================================
WORKDIR /app
COPY . /app

# ============================================================
# HuggingFace / Transformers – sandbox safe
# ============================================================
ENV HF_HOME=/app/models
ENV TRANSFORMERS_CACHE=/app/models
ENV PYTHONUNBUFFERED=1

# ============================================================
# Python deps
# ============================================================
RUN pip install --no-cache-dir --upgrade pip && \
    pip uninstall -y transformers || true && \
    pip install --no-cache-dir transformers==4.35.2 && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================
# ⛔ NESSUN ENTRYPOINT ⛔
# Hone / Sandbox Runner passa il comando
# ============================================================

