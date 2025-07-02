import requests

def generate_tests_ollama(code: str, prompt: str) -> str:
    full_prompt = f"{prompt}\n\n```c\n{code}\n```"
    payload = {
        "model": "codellama",  # or use "phi" if it's too slow
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["response"]
    except requests.Timeout:
        print("❌ Timeout: Model took too long to respond.")
        return ""
    except Exception as e:
        print(f"❌ Error querying Ollama API: {e}")
        return ""
