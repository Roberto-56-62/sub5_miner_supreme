FROM python:3.10-slim

# ============================================================
# System dependencies
# ============================================================
RUN apt-get update && \
    apt-get install -y git wget ca-certificates && \
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

# ⏱️ timeout e retry ALTI (senza hf_transfer)
ENV HF_HUB_DOWNLOAD_TIMEOUT=300
ENV HF_HUB_ETAG_TIMEOUT=300
ENV HF_HUB_MAX_RETRIES=5

ENV PYTHONUNBUFFERED=1

# ============================================================
# Python deps
# ============================================================
RUN pip install --no-cache-dir --upgrade pip && \
    pip uninstall -y transformers || true && \
    pip install --no-cache-dir transformers==4.35.2 && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================
# NO ENTRYPOINT / CMD
# ============================================================

