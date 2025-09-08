import serpapi
import os
import requests
import json
import csv

def search(keyword:str) -> dict:
    search = serpapi.search({
        "q": keyword,
        "api_key": os.getenv("SERPAPI_API_KEY")
    })
    return search

def handle_search_result(word:str, result:dict) -> None:
    answer_box = result.get("answer_box", {})

    if answer_box.get("type") != "dictionary_results":
        return {}

    print(json.dumps(answer_box, indent=4))

    definition = answer_box.get("definitions", [])
    string_definition = ""
    for index, defi in enumerate(definition):
        string_definition += f"\t{index + 1}. {defi}\n"
    syllables = answer_box.get("examples", [])[0]
    word_type = answer_box.get("word_type")
    examples = answer_box.get("examples", [])[1:]
    string_example = ""
    for index, example in enumerate(examples):
        if index % 2 == 0:
            string_example += f"{example} - "
        else:
            string_example += f"{example}\n"
    synonyms = []
    antonyms = []

    return {
        "column_a": f"{word} {syllables}\n{string_example}",
        "column_b": f"Part of Speech: {word_type}\nDefinition:\n{string_definition}\nSynonyms: {', '.join(synonyms)}\nAntonyms: {', '.join(antonyms)}",
    }

def main():
    try:
        new_words_url = "https://raw.githubusercontent.com/manh-td/new-words/refs/heads/main/words.txt"
        response = requests.get(new_words_url)
    except requests.RequestException as e:
        raise ValueError(f"Error fetching new words: {e}")

    row = []
    if response.status_code == 200:
        words = response.text.splitlines()
        for word in words:
            word = word.split(" ")[0].strip()
            result = search(word)
            handled_result = handle_search_result(word,result)
            row.append(handled_result)
    else:
        print(f"Error fetching new words: {response.status_code}")

    with open("output.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["column_a", "column_b"])
        writer.writeheader()
        for r in row:
            if r:
                writer.writerow(r)

if __name__ == "__main__":
    main()