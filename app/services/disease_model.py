from __future__ import annotations

CONDITION_RULES: dict[str, set[str]] = {
    "Akute Atemwegsinfektion": {"fever", "cough", "sore_throat"},
    "Gastroenteritis": {"nausea", "vomiting", "diarrhea", "abdominal_pain"},
    "Migraene / Spannungskopfschmerz": {"headache", "nausea"},
    "Kardiopulmonale Warnkonstellation": {"chest_pain", "shortness_of_breath"},
}


def predict_condition(normalized_symptoms: list[str]) -> tuple[str, float]:
    symptom_set = set(normalized_symptoms)

    best_name = "Unspezifische Beschwerdesymptomatik"
    best_score = 0.0

    for condition, rule_symptoms in CONDITION_RULES.items():
        if not rule_symptoms:
            continue
        overlap = len(symptom_set.intersection(rule_symptoms))
        score = overlap / len(rule_symptoms)
        if score > best_score:
            best_score = score
            best_name = condition

    return best_name, round(best_score, 2)
