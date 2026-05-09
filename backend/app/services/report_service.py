from datetime import datetime


def generate_doctor_report_de(
    patient_name: str | None,
    raw_message: str,
    detected_language: str,
    normalized_symptoms: list[str],
    emergency: bool,
    emergency_reason: str,
    predicted_disease: str,
    confidence: float,
) -> str:
    patient = patient_name or "Unbekannt"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    status = "JA" if emergency else "NEIN"

    return (
        f"MediBridge AI Bericht ({now})\\n"
        f"Patient: {patient}\\n"
        f"Eingabesprache: {detected_language}\\n"
        f"Originaltext: {raw_message}\\n"
        f"Normalisierte Symptome: {', '.join(normalized_symptoms)}\\n"
        f"Notfallindikator: {status}\\n"
        f"Begruendung: {emergency_reason}\\n"
        f"Wahrscheinliche Erkrankung: {predicted_disease} (Konfidenz {confidence:.2f})\\n"
        "Hinweis: KI-Ersteinschaetzung, ersetzt keine aerztliche Diagnose."
    )
