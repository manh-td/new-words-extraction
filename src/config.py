from pathlib import Path

CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
MODEL = "phi3:mini"
PROMPTS = {
    "part_of_speech": """You are an English dictionary assistant.
Given the following word "{word}".
Answer only the **part of speech** (e.g., noun, verb, adjective) as plain text (no JSON, no explanation).""",

    "definitions": """You are an English dictionary assistant.
Given the following word "{word}".
Answer only the **definitions** (maximum 2).
Format your response exactly like this:
definition 1; definition 2
(no JSON, no explanation).""",

    "examples": """You are an English dictionary assistant.
Given the following word "{word}".
Answer only short example sentences of how to use the word in English (maximum 2).
Format your response exactly like this:
sentence 1; sentence 2
(no JSON, no explanation).""",

    "synonyms": """You are an English dictionary assistant.
Given the following word "{word}".
Answer only **synonyms** (maximum 2). If there are multiple, join them into a single string separated by semicolons (; ).
Respond with plain text only (no JSON, no explanation).""",

    "antonyms": """You are an English dictionary assistant.
Given the following word "{word}".
Answer only **antonyms** (maximum 2). If there are multiple, join them into a single string separated by semicolons (; ).
Respond with plain text only (no JSON, no explanation)."""
}
LLM_TIMEOUT = 5 * 60
NEW_WORD_URL = "https://raw.githubusercontent.com/manh-td/new-words/refs/heads/main/words.txt"
OUTPUT_FILE = "output.csv"

DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"