import requests
import json
import csv
from pathlib import Path
import subprocess
from .config import *

def query_llm(word: str, model: str = MODEL) -> dict:
    """
    Query a local LLM (via Ollama) for a definition, examples, and synonyms.
    Uses local cache to avoid repeated queries.
    """
    cache_path = CACHE_DIR / f"{word.lower()}.json"
    if cache_path.exists():
        with open(cache_path, "r", encoding="utf-8") as f:
            return json.load(f)

    prompt = PROMPT.format(word=word)

    print(f"🧠 Querying LLM for: {word}")
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
            parsed = {"definitions": [output]}

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)

        return parsed

    except subprocess.TimeoutExpired:
        return {"definitions": ["(Timeout while querying local LLM)"]}
    except Exception as e:
        return {"definitions": [f"(Error: {e})"]}


def handle_llm_result(word: str, result: dict) -> dict:
    try:
        phonetic = result.get("phonetic", "")
        word_type = result.get("word_type", "")
        definitions = result.get("definitions", [])
        examples = result.get("examples", [])
        synonyms = result.get("synonyms", [])
        antonyms = result.get("antonyms", [])

        string_definition = "\n".join([f"\t{i+1}. {d}" for i, d in enumerate(definitions)])
        string_example = "\n".join(examples)

        return {
            "column_a": f"{word} {phonetic}\nExamples:\n{string_example}",
            "column_b": f"Part of Speech: {word_type}\nDefinition:\n{string_definition}\nSynonyms: {', '.join(synonyms)}\nAntonyms: {', '.join(antonyms)}",
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
            handled_result = handle_llm_result(word, result)
            if len(handled_result) > 0:
                rows.append(handled_result)
    else:
        print(f"Error fetching new words: {response.status_code}")

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["column_a", "column_b"])
        writer.writeheader()
        for r in rows:
            if r:
                writer.writerow(r)

    print("✅ Finished writing to output.csv")


if __name__ == "__main__":
    main()