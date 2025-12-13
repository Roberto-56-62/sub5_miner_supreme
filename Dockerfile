FROM python:3.10-slim

# ===============================
# System dependencies
# ===============================
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        wget \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ===============================
# Working directory
# ===============================
WORKDIR /app

# ===============================
# Copy miner source code
# ===============================
COPY . /app

# ===============================
# Install Python dependencies
# ===============================
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================================
# ⚠️ IMPORTANT
# ----------------------------------------------------------
# DO NOT use ENTRYPOINT.
# The Subnet 5 runner will explicitly call:
#  - arc_prep.py   (internet ENABLED)
#  - arc_main.py   (internet DISABLED)
#
# Leaving CMD as "bash" allows the runner
# to control which phase is executed.
# ==========================================================
CMD ["bash"]

