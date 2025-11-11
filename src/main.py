import requests
import csv

from .config import *
from .dictionary import get_word_definition, process_word_definition
from .llm import query_llm, get_word_form

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
            
            word = get_word_form(word)
            dictionary = get_word_definition(word)
            if "error" in dictionary:
                continue
            
            dictionary = process_word_definition(dictionary)
            results = query_llm(word, dictionary)
            for result in results:
                rows.append({
                    "column_a": f"{word} {result['phonetic']}\nExamples: {result['examples']}",
                    "column_b": f"Part of Speech: {result['part_of_speech']}\nDefinition: {result['definitions']}\nSynonyms: {result['synonyms']}\nAntonyms: {result['antonyms']}\nRelated forms: {result['related_forms']}",
                })

    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["column_a", "column_b"])
        writer.writeheader()
        for r in rows:
            if r:
                writer.writerow(r)

if __name__ == "__main__":
    main()
