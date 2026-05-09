SYMPTOM_LEXICON = {
    "fever": ["fever", "fieber", "حمى", "حرارة", "ates"],
    "cough": ["cough", "husten", "سعال", "كحة", "öksürük", "oksuruk"],
    "shortness_of_breath": ["shortness of breath", "atemnot", "ضيق تنفس", "nefes darligi", "nefes"],
    "chest_pain": ["chest pain", "brustschmerzen", "ألم صدر", "göğüs ağrısı", "gogus agrisi"],
    "headache": ["headache", "kopfschmerzen", "صداع", "baş ağrısı", "bas agrisi"],
    "sore_throat": ["sore throat", "halsschmerzen", "ألم حلق", "bogaz agrisi"],
    "nausea": ["nausea", "übelkeit", "غثيان", "mide bulantisi"],
    "vomiting": ["vomiting", "erbrechen", "قيء", "kusma"],
    "diarrhea": ["diarrhea", "durchfall", "إسهال", "ishal"],
    "abdominal_pain": ["abdominal pain", "bauchschmerzen", "ألم بطن", "karin agrisi"],
}


def normalize_symptoms(text: str) -> list[str]:
    lower = text.lower()
    found: list[str] = []
    for canonical, variants in SYMPTOM_LEXICON.items():
        if any(v in lower for v in variants):
            found.append(canonical)
    return found or ["unspecified_symptoms"]
