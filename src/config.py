from pathlib import Path

CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
MODEL = "phi3:mini"
PROMPT = """
You are an English dictionary assistant.
You are given a JSON dictionary entry as context, containing fields about a word.

Context (from Free Dictionary API):
{dictionary}

Your task:
- Review the given data carefully.
- Use **only** the information available in the dictionary entry as your primary source.
- If a field in the output is missing or empty in the context, infer or fill it in briefly and plausibly based on general English knowledge.
- If a field is already present and complete, preserve its content faithfully without rewriting it.

Output requirements:
- Include these exact fields: phonetic, word_type, definitions, examples, synonyms, antonyms.
- Each field must be a string.
- Multiple items (e.g., definitions, examples, synonyms, antonyms) must be joined into a single string separated by semicolons.
- Ensure the output is valid JSON and contains *only* the specified keys.
- Do not include explanations, reasoning, or extra text — output pure JSON only.

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