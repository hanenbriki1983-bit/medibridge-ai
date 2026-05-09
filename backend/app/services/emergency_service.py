EMERGENCY_RULES = {
    "chest_pain": "Brustschmerz erkannt",
    "shortness_of_breath": "Atemnot erkannt",
}


def detect_emergency(symptoms: list[str]) -> tuple[bool, str]:
    symptom_set = set(symptoms)

    if {"chest_pain", "shortness_of_breath"}.issubset(symptom_set):
        return True, "Kombination aus Brustschmerz und Atemnot - akuter Notfallverdacht."

    for key, reason in EMERGENCY_RULES.items():
        if key in symptom_set:
            return True, f"Warnsignal: {reason}."

    return False, "Keine unmittelbaren Notfallzeichen erkannt."
