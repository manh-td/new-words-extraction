import requests
import csv
import subprocess
import hashlib
import json

from .config import *
from .dictionary import get_word_definition, process_word_definition

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
            return cached_data.get("response", "")

        # If not cached, call the model
        print(f"[LLM RUN] {prompt}")
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=LLM_TIMEOUT
        )
        output = result.stdout.strip()

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

def main():
    try:
        response = requests.get(NEW_WORD_URL)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Error fetching new words: {e}")

    rows = []
    if response.status_code == 200:
        words = response.text.splitlines()
        for word in words:
            word = word.split(" ")[0].strip()
            if not word:
                continue
            
            dictionary = get_word_definition(word)
            if "error" in dictionary:
                continue
            
            dictionary = process_word_definition(dictionary)
            results = query_llm(word, dictionary)
            for result in results:
                rows.append({
                    "column_a": f"{word} {result['phonetic']}\nExamples: {result['examples']}",
                    "column_b": f"Part of Speech: {result['part_of_speech']}\nDefinition: {result['definitions']}\nSynonyms: {result['synonyms']}\nAntonyms: {result['antonyms']}",
                })

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["column_a", "column_b"])
        writer.writeheader()
        for r in rows:
            if r:
                writer.writerow(r)

if __name__ == "__main__":
    main()
