from pathlib import Path

CACHE_DIR = Path("./cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
MODEL = "qwen3:1.7b"
PROMPTS = {
    "examples": """You are an English dictionary assistant.  
Given the word "{word}" ({part_of_speech}), provide one short example sentence showing how it is used in English.  
Respond only with the sentence — no explanations or extra text.""",

    "synonyms": """You are an English dictionary assistant.  
Given the word "{word}" ({part_of_speech}), provide up to two synonyms.  
If there are multiple, join them into a single string separated by semicolons (;).  
Respond with plain text only — no explanations or extra text.""",

    "antonyms": """You are an English dictionary assistant.  
Given the word "{word}" ({part_of_speech}), provide up to two antonyms.  
If there are multiple, join them into a single string separated by semicolons (;).  
Respond with plain text only — no explanations or extra text.""",

    "basic_form": """Return only the basic (base) form of this English word: "{word}".
Output just the word, nothing else.""",

    "related_forms": """You are an English dictionary assistant.  
Given the word "{word}" ({part_of_speech}), provide up to 3 related word forms, including inflections, derivatives, or closely related words.  
Do not include the original word itself in the list.  
Respond with a single flat list of words in plain text, separated by semicolons (;).  
Do not include definitions, examples, or any extra text."""
}
LLM_TIMEOUT = 5 * 60
NEW_WORD_URL = "https://raw.githubusercontent.com/manh-td/new-words/refs/heads/main/words.txt"
OUTPUT_FILE = "output.csv"

DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"