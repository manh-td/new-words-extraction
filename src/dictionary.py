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


# Example usage
if __name__ == "__main__":
    result = get_word_definition("apparent")
    if "error" in result:
        print(result["error"])
    else:
        print(json.dumps(result, indent=4))
