from transformers import AutoTokenizer, AutoModelForCausalLM
from utilities.logger import log


def load_model_and_tokenizer(repo_id, device):
    log(f"📦 Carico modello HuggingFace: {repo_id}", "yellow")

    tokenizer = AutoTokenizer.from_pretrained(repo_id)
    model = AutoModelForCausalLM.from_pretrained(
        repo_id,
        torch_dtype="auto",
        device_map=device
    )

    return model, tokenizer

