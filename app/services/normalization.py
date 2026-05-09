from __future__ import annotations

import re

SYMPTOM_MAP: dict[str, list[str]] = {
    "fever": ["fever", "fieber", "حمى", "حرارة"],
    "cough": ["cough", "husten", "سعال", "كحة"],
    "chest_pain": ["chest pain", "brustschmerzen", "ألم صدر", "وجع صدر"],
    "shortness_of_breath": ["shortness of breath", "atemnot", "ضيق تنفس", "نهجان"],
    "headache": ["headache", "kopfschmerzen", "صداع"],
    "nausea": ["nausea", "übelkeit", "غثيان"],
    "vomiting": ["vomiting", "erbrechen", "قيء", "استفراغ"],
    "abdominal_pain": ["abdominal pain", "bauchschmerzen", "ألم بطن", "مغص"],
    "sore_throat": ["sore throat", "halsschmerzen", "التهاب حلق", "ألم حلق"],
    "diarrhea": ["diarrhea", "durchfall", "إسهال"],
}


def normalize_symptoms(text: str) -> list[str]:
    normalized: list[str] = []
    clean_text = re.sub(r"\s+", " ", text.lower()).strip()

    for canonical, variants in SYMPTOM_MAP.items():
        if any(variant in clean_text for variant in variants):
            normalized.append(canonical)

    if not normalized:
        normalized.append("unspecified_symptoms")

    return normalized
