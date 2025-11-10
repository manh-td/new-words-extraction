import requests
import csv
import subprocess
from .config import *
from .dictionary import get_word_definition, process_word_definition

def infer_llm(prompt:str, model:str = MODEL) -> str:
    try:
        print(prompt)
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=LLM_TIMEOUT
        )
        print(result.stdout.strip())
        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        return None

def query_llm(word:str, dictionaries: list[str]) -> dict|None:
    for dictionary in dictionaries:
        for key, value in dictionary.items():
            if key == "part_of_speech" and value == "":
                prompt = PROMPTS["part_of_speech"].format(word=word)
                response = infer_llm(prompt)
                dictionary[key] = response
            if key == "definitions" and value == "":
                prompt = PROMPTS["definitions"].format(word=word)
                response = infer_llm(prompt)
                dictionary[key] = response
            if key == "examples" and value == "":
                prompt = PROMPTS["examples"].format(word=word)
                response = infer_llm(prompt)
                dictionary[key] = response
            if key == "synonyms" and value == "":
                prompt = PROMPTS["synonyms"].format(word=word)
                response = infer_llm(prompt)
                dictionary[key] = response
            if key == "antonyms" and value == "":
                prompt = PROMPTS["antonyms"].format(word=word)
                response = infer_llm(prompt)
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
                return None
            
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
