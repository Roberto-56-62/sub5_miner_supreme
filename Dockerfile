FROM python:3.10-slim

# Install system deps
RUN apt-get update && apt-get install -y git wget && apt-get clean

# Create workdir
WORKDIR /app

# Copy miner code
COPY . /app

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Default entrypoint (arc_main.py)
ENTRYPOINT ["python3", "arc_main.py"]

