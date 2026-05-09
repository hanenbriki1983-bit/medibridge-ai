from __future__ import annotations

from datetime import datetime


def build_doctor_report_de(
    patient_name: str | None,
    raw_text: str,
    detected_language: str,
    normalized_symptoms: list[str],
    risk_level: str,
    risk_reason: str,
    predicted_condition: str,
    prediction_confidence: float,
) -> str:
    patient = patient_name or "Unbekannt"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return (
        f"MediBridge AI Kurzbericht ({now})\\n"
        f"Patient: {patient}\\n"
        f"Erkannte Eingabesprache: {detected_language}\\n"
        f"Rohbeschreibung: {raw_text}\\n"
        f"Medizinisch normalisierte Symptome: {', '.join(normalized_symptoms)}\\n"
        f"Risikostufe: {risk_level}\\n"
        f"Begruendung: {risk_reason}\\n"
        f"Vermutete Diagnose: {predicted_condition} (Konfidenz: {prediction_confidence:.2f})\\n"
        "Hinweis: Dies ist eine KI-gestuetzte Ersteinschaetzung und ersetzt keine ärztliche Diagnose."
    )
