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

Format your response as pure JSON with keys exactly like this:
{{
    "phonetic": "...",
    "word_type": "...",
    "definitions": ["..."],
    "examples": ["..."],
    "synonyms": ["..."],
    "antonyms": ["..."]
}}
"""
LLM_TIMEOUT = 3 * 60
NEW_WORD_URL = "https://raw.githubusercontent.com/manh-td/new-words/refs/heads/main/words.txt"
OUTPUT_FILE = "output.csv"