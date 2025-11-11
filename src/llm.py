import subprocess
import hashlib
import json

from .config import *

def infer_llm(prompt: str, model: str = MODEL) -> str:
    """
    Runs an LLM query using ollama, with caching based on a hash of the prompt.
    Cached results are stored in .cache/{hash}.json
    """
    try:
        # Generate a unique hash for the prompt and model
        prompt_id = hashlib.sha256(f"{model}:{prompt}".encode("utf-8")).hexdigest()
        cache_path = CACHE_DIR / "prompt_cache" 
        cache_path.mkdir(parents=True, exist_ok=True)
        cache_path = cache_path / f"{prompt_id}.json"

        # Check cache first
        if cache_path.exists():
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                response = cached_data.get("response", "")
                response = response.split("\n...done thinking.\n\n")[-1]
            return response

        # If not cached, call the model
        print(f"[LLM RUN] {prompt}")
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=LLM_TIMEOUT
        )
        output = result.stdout.strip()
        output = output.split("\n...done thinking.\n\n")[-1]

        # Save response to cache
        with open(str(cache_path), "w", encoding="utf-8") as f:
            json.dump({"prompt": prompt, "response": output}, f, ensure_ascii=False, indent=2)

        print(f"[CACHED] {cache_path}")
        return output

    except subprocess.TimeoutExpired:
        print("[TIMEOUT] LLM request timed out.")
        return None
    except Exception as e:
        print(f"[ERROR] infer_llm: {e}")
        return None

def query_llm(word:str, dictionaries: list[str]) -> dict|None:
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            if key == "definitions" and value == "":
                prompt = PROMPTS["definitions"].format(word=word, part_of_speech=dictionary["part_of_speech"])
                response = infer_llm(prompt)
                if response:
                    dictionary[key] = response
            if key == "examples" and value == "":
                prompt = PROMPTS["examples"].format(word=word, part_of_speech=dictionary["part_of_speech"])
                response = infer_llm(prompt)
                if response:
                    dictionary[key] = response
            if key == "synonyms" and value == "":
                prompt = PROMPTS["synonyms"].format(word=word, part_of_speech=dictionary["part_of_speech"])
                response = infer_llm(prompt)
                if response:
                    dictionary[key] = response
            if key == "antonyms" and value == "":
                prompt = PROMPTS["antonyms"].format(word=word, part_of_speech=dictionary["part_of_speech"])
                response = infer_llm(prompt)
                if response:
                    dictionary[key] = response

    return dictionaries

def get_word_form(word:str) -> str|None:
    prompt = PROMPTS["basic_form"].format(word=word)
    response = infer_llm(prompt)
    if response:
        return response
    return None

if __name__ == "__main__":
    print(get_word_form("assailed"))