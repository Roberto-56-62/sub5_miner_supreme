FROM python:3.10-slim

# --------------------------------------------------
# Ambiente base Hone
# --------------------------------------------------
WORKDIR /app
COPY . /app

# --------------------------------------------------
# Dipendenze
# --------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------------------
# IMPORTANTISSIMO
# ❌ NESSUN CMD
# ❌ NESSUN ENTRYPOINT
# Hone inietta lui il comando:
#   python arc_main.py
# --------------------------------------------------

