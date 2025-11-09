import requests
import json
import csv
import subprocess
from .config import *
from .dictionary import get_word_definition

def query_llm(word: str, model: str = MODEL) -> dict|None:
    """
    Query a local LLM (via Ollama) for a definition, examples, and synonyms.
    Uses local cache to avoid repeated queries.
    """
    cache_path = CACHE_DIR / f"{word.lower()}.json"
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    dictionary=get_word_definition(word)
    if "error" in dictionary:
        return None
    
    prompt = PROMPT.format(word=word, dictionary=json.dumps(dictionary, indent=4))

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=LLM_TIMEOUT
        )
        output = result.stdout.strip()

        # Try to extract JSON safely
        try:
            json_start = output.find("{")
            json_end = output.rfind("}") + 1
            parsed = json.loads(output[json_start:json_end])
        except Exception:
            return None

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)

        return parsed

    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        return None


def handle_llm_result(word: str, result: dict) -> dict:
    try:
        phonetic = result.get("phonetic", "")
        word_type = result.get("word_type", "")
        definitions = result.get("definitions", "")
        examples = result.get("examples", "")
        synonyms = result.get("synonyms", "")
        antonyms = result.get("antonyms", "")

        return {
            "column_a": f"{word} {phonetic}\nExamples: {examples}",
            "column_b": f"Part of Speech: {word_type}\nDefinition: {definitions}\nSynonyms: {synonyms}\nAntonyms: {antonyms}",
        }
    except Exception as e:
        return {}


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

            result = query_llm(word)
            if result:
                handled_result = handle_llm_result(word, result)
                if len(handled_result) > 0:
                    rows.append(handled_result)

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["column_a", "column_b"])
        writer.writeheader()
        for r in rows:
            if r:
                writer.writerow(r)

if __name__ == "__main__":
    main()
