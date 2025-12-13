FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime

# Evita qualsiasi lookup HF
ENV HF_HUB_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1
ENV TOKENIZERS_PARALLELISM=false

WORKDIR /app

# Copia codice
COPY . /app

# Installa SOLO dipendenze leggere
RUN pip install --no-cache-dir \
    transformers>=4.36.0 \
    accelerate \
    huggingface_hub

# Entry
ENTRYPOINT ["python3", "arc_main.py"]

