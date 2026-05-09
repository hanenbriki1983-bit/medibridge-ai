import re

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")
TURKISH_CHARS_RE = re.compile(r"[ğüşöçıİĞÜŞÖÇ]")
GREEK_RE = re.compile(r"[\u0370-\u03FF]")
CYRILLIC_RE = re.compile(r"[\u0400-\u04FF]")
GERMAN_HINTS = {"und", "ich", "habe", "schmerzen", "fieber", "atemnot"}
TURKISH_HINTS = {"ve", "ben", "ates", "öksürük", "nefes", "agrı"}
FRENCH_HINTS = {"et", "jai", "douleur", "fievre", "toux", "depuis"}
RUSSIAN_HINTS = {"и", "у", "меня", "боль", "жар", "кашель"}


def detect_language(text: str) -> str:
    lower = text.lower()
    tokens = re.findall(r"\w+", lower)

    if ARABIC_RE.search(text):
        return "ar"
    if GREEK_RE.search(text):
        return "el"
    if CYRILLIC_RE.search(text) or sum(w in RUSSIAN_HINTS for w in tokens) >= 2:
        return "ru"
    if TURKISH_CHARS_RE.search(text) or sum(w in TURKISH_HINTS for w in re.findall(r"\w+", lower)) >= 2:
        return "tr"
    if sum(w in GERMAN_HINTS for w in tokens) >= 2:
        return "de"
    if sum(w in FRENCH_HINTS for w in tokens) >= 2:
        return "fr"
    return "en"
