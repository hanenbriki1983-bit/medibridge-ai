from __future__ import annotations

import re

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")

COMMON_GERMAN_WORDS = {
    "und",
    "ich",
    "habe",
    "seit",
    "schmerzen",
    "fieber",
    "atemnot",
    "heute",
    "tage",
}


def detect_language(text: str) -> str:
    lower_text = text.lower()
    if ARABIC_RE.search(text):
        return "ar"

    score_de = sum(1 for token in re.findall(r"\w+", lower_text) if token in COMMON_GERMAN_WORDS)
    if score_de >= 2:
        return "de"

    return "en"
