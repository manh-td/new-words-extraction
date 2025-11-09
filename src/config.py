from pathlib import Path

CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
MODEL = "gpt-oss:20b"
PROMPT = """You are an English dictionary assistant.

You are provided with a JSON dictionary entry containing information about the word "{word}".

Context (from Free Dictionary API):
{dictionary}

Your task:
Extract and complete the following fields for the given word:
- phonetic
- word_type
- definitions
- examples
- synonyms
- antonyms

Output instructions:
- Return **only** a valid JSON object containing exactly these six fields.
- Each field value must be a non-empty string.
- If a field contains multiple items (e.g., multiple definitions, examples, synonyms, or antonyms), join them into a single string separated by semicolons.
- Do **not** include any explanations, reasoning, or extra text — output the JSON object only.

Output format:
{{
    "phonetic": "string",
    "word_type": "string",
    "definitions": "string",
    "examples": "string",
    "synonyms": "string",
    "antonyms": "string"
}}
"""
LLM_TIMEOUT = 5 * 60
NEW_WORD_URL = "https://raw.githubusercontent.com/manh-td/new-words/refs/heads/main/words.txt"
OUTPUT_FILE = "output.csv"

DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"