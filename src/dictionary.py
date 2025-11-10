import requests
import json
from .config import DICTIONARY_API, CACHE_DIR

def get_word_definition(word: str):
    """
    Fetch the definition, phonetics, and examples of a word
    from the Free Dictionary API (dictionaryapi.dev).
    Uses local caching to avoid redundant API calls.

    Args:
        word (str): The word to look up.

    Returns:
        dict: A dictionary containing word details or an error message.
    """
    word = word.lower().strip()
    cache_file = CACHE_DIR / "apis"
    cache_file.mkdir(parents=True, exist_ok=True)
    cache_file = cache_file / f"{word}.json"

    # ✅ 1. Check cache first
    if cache_file.exists():
        try:
            with cache_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            cache_file.unlink(missing_ok=True)  # delete invalid cache

    # ✅ 2. Fetch from API if not cached
    response = requests.get(DICTIONARY_API.format(word=word))

    if response.status_code != 200:
        return {"error": f"Word '{word}' not found or API error."}

    try:
        data = response.json()[0]
    except (ValueError, IndexError, KeyError):
        return {"error": "Invalid API response structure."}

    # Remove unnecessary fields if present
    data.pop("license", None)

    # ✅ 3. Cache successful response
    try:
        with cache_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass  # ignore cache write errors gracefully

    return data

def process_word_definition(api_result: dict, max_list: int = 2) -> dict:
    cache_file = CACHE_DIR / "processed_apis"
    cache_file.mkdir(parents=True, exist_ok=True)
    cache_file = cache_file / f"{api_result['word']}.json"

    if cache_file.exists():
        try:
            with cache_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            cache_file.unlink(missing_ok=True)  # delete invalid cache

    outputs = []

    # Extract phonetic (limit to max_list)
    phonetic = api_result.get("phonetic", "")
    if not phonetic:
        phonetics = api_result.get("phonetics", [])
        phonetic_list = [p.get("text", "") for p in phonetics if "text" in p][:max_list]
        phonetic = "; ".join(phonetic_list)

    meanings = api_result.get("meanings", [])
    for meaning in meanings[:max_list]:
        part_of_speech = meaning.get("partOfSpeech", "")

        definitions = meaning.get("definitions", [])[:max_list]
        definition_texts = [d.get("definition", "") for d in definitions]
        example_texts = [d.get("example", "") for d in definitions if d.get("example")]

        synonyms = meaning.get("synonyms", [])[:max_list]
        antonyms = meaning.get("antonyms", [])[:max_list]

        outputs.append({
            "phonetic": phonetic,
            "part_of_speech": part_of_speech,
            "definitions": "; ".join(definition_texts),
            "examples": "; ".join(example_texts),
            "synonyms": "; ".join(synonyms),
            "antonyms": "; ".join(antonyms),
        })

    try:
        with cache_file.open("w", encoding="utf-8") as f:
            json.dump(outputs, f, ensure_ascii=False, indent=2)
    except OSError:
        pass  # ignore cache write errors gracefully

    return outputs

# Example usage
if __name__ == "__main__":
    api_result = get_word_definition("apparent")
    processed_api = process_word_definition(api_result)
    print(json.dumps(processed_api, indent=4))
