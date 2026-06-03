import runpod
import subprocess
import requests
import time
import os

# Test avec petit modèle, ou DeepSeek si présent sur le volume
TEST_MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf"
TEST_MODEL_PATH = "/tmp/test-model.gguf"
DEEPSEEK_PATH = "/runpod-volume/DeepSeek-V3.1-UD-TQ1_0.gguf"

def get_model_path():
    if os.path.exists(DEEPSEEK_PATH):
        print(f"Using DeepSeek: {DEEPSEEK_PATH}")
        return DEEPSEEK_PATH
    else:
        print("DeepSeek not found, downloading test model...")
        subprocess.run(["curl", "-L", "-o", TEST_MODEL_PATH, TEST_MODEL_URL], check=True)
        return TEST_MODEL_PATH

MODEL_PATH = None  # Set at startup
PORT = 8080
server = None

def start_server(model_path):
    global server

    # Config différente selon le modèle
    if "DeepSeek" in model_path:
        cmd = [
            "llama-server",
            "--model", model_path,
            "--host", "0.0.0.0",
            "--port", str(PORT),
            "--n-gpu-layers", "999",
            "-ot", "ffn_.*_exp=CPU",
            "--ctx-size", "8192",
            "--jinja",
        ]
    else:
        # Petit modèle de test - config simple
        cmd = [
            "llama-server",
            "--model", model_path,
            "--host", "0.0.0.0",
            "--port", str(PORT),
            "--n-gpu-layers", "999",
        ]

    print(f"Starting: {' '.join(cmd)}")
    server = subprocess.Popen(cmd)

    # Attendre que le serveur soit prêt
    for _ in range(150):
        try:
            r = requests.get(f"http://localhost:{PORT}/health")
            if r.status_code == 200:
                return True
        except:
            pass
        time.sleep(2)
    return False

def handler(job):
    inp = job["input"]

    if "messages" in inp:
        r = requests.post(f"http://localhost:{PORT}/v1/chat/completions", json={
            "messages": inp["messages"],
            "max_tokens": inp.get("max_tokens", 512),
        })
    else:
        r = requests.post(f"http://localhost:{PORT}/completion", json={
            "prompt": inp.get("prompt", ""),
            "n_predict": inp.get("max_tokens", 512),
        })

    return r.json()

if __name__ == "__main__":
    model_path = get_model_path()
    if not start_server(model_path):
        raise RuntimeError("Server failed to start")
    runpod.serverless.start({"handler": handler})
