from __future__ import annotations


def assess_risk(normalized_symptoms: list[str]) -> tuple[str, str]:
    severe_flags = {"chest_pain", "shortness_of_breath"}
    moderate_flags = {"fever", "vomiting", "abdominal_pain"}

    if severe_flags.issubset(set(normalized_symptoms)):
        return "high", "Kombination aus Brustschmerz und Atemnot (Notfallverdacht)."

    if severe_flags.intersection(normalized_symptoms):
        return "medium", "Warnsymptom erkannt; zeitnahe ärztliche Abklärung empfohlen."

    if len(moderate_flags.intersection(normalized_symptoms)) >= 2:
        return "medium", "Mehrere systemische Symptome erkannt."

    return "low", "Keine unmittelbaren Red Flags erkannt."
