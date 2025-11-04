from pathlib import Path

CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
MODEL = "phi3:mini"
PROMPT = """
You are an English dictionary assistant.
Define the word "{word}" clearly and concisely.
Include:
- Part of speech
- Phonetic transcription (if known)
- Short definition(s)
- Two example sentences
- Common synonyms and antonyms

Ensure that:
- All fields are strings.
- Multiple items (e.g., definitions, examples, synonyms, antonyms) are combined into a single string separated by semicolons.
- The output must be valid JSON and contain *only* the following keys.

Format your response as pure JSON with this exact structure:
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
