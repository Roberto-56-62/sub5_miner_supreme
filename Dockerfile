FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y git wget && apt-get clean

WORKDIR /app
COPY . /app

# 🔥 FORZA DOWNGRADE (prima di tutto)
RUN pip install --no-cache-dir --upgrade pip \
 && pip uninstall -y transformers \
 && pip install --no-cache-dir transformers==4.35.2

# 🔒 install resto deps
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "arc_main.py"]

