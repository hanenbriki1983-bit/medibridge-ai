import json

from fastapi import APIRouter, HTTPException

from app.agents.triage_agent import triage_agent_decision
from app.database.db import insert_case
from app.ml.predictor import predict_disease
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.emergency_service import detect_emergency
from app.services.language_service import detect_language
from app.services.report_service import generate_doctor_report_de
from app.services.symptom_service import normalize_symptoms

router = APIRouter(prefix="/chat", tags=["chat"])

LANG_REPLY = {
    "ar": "تم استلام المعلومات الطبية الأولية. هذه المعلومات للتوعية فقط، استشر طبيباً مختصاً في الحالات الخطيرة.",
    "de": "Die medizinischen Erstinformationen wurden erfasst. Diese Informationen dienen nur der Aufklaerung; bei ernsten Faellen bitte aerztlich abklaeren.",
    "en": "Initial medical information has been recorded. This information is for awareness only; consult a qualified doctor for serious cases.",
    "tr": "Ilk tibbi bilgiler kaydedildi. Bu bilgiler yalnizca bilgilendirme amaclidir; ciddi durumlarda uzman doktora basvurun.",
    "fr": "Les informations medicales initiales ont ete enregistrees. Ces informations sont uniquement educatives; consultez un medecin en cas grave.",
    "el": "Τα αρχικα ιατρικα στοιχεια καταχωρηθηκαν. Οι πληροφοριες ειναι μονο για ενημερωση· σε σοβαρες περιπτωσεις συμβουλευτειτε γιατρο.",
    "ru": "Начальная медицинская информация получена. Эти сведения носят ознакомительный характер; при серьезных состояниях обратитесь к врачу.",
}

FOLLOW_UP_PROMPTS = {
    "ar": "يرجى استكمال: مدة الأعراض، شدتها (1-10)، العمر، والأمراض المزمنة أو الأدوية الحالية.",
    "de": "Bitte ergaenzen Sie: Symptomdauer, Schweregrad (1-10), Alter sowie Vorerkrankungen/Medikation.",
    "en": "Please add: symptom duration, severity (1-10), age, and chronic diseases/current medications.",
    "tr": "Lutfen ekleyin: semptom suresi, siddet (1-10), yas, kronik hastaliklar/mevcut ilaclar.",
    "fr": "Veuillez ajouter : duree des symptomes, gravite (1-10), age et maladies chroniques/traitements en cours.",
    "el": "Παρακαλω προσθεστε: διαρκεια συμπτωματων, ενταση (1-10), ηλικια και χρονια νοσηματα/φαρμακα.",
    "ru": "Пожалуйста, добавьте: длительность симптомов, выраженность (1-10), возраст и хронические заболевания/текущие лекарства.",
}


def determine_human_verification(emergency: bool, confidence: float) -> tuple[bool, str]:
    if emergency:
        return True, "Emergency signal detected."
    if confidence < 0.55:
        return True, "Low model confidence for disease prediction."
    return False, "Not required."


def needs_more_information(normalized: list[str]) -> bool:
    if "unspecified_symptoms" in normalized:
        return True
    return len(normalized) < 2


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not payload.consent_accepted:
        raise HTTPException(status_code=400, detail="Consent is required before clinical processing.")

    language = detect_language(payload.message)
    normalized = normalize_symptoms(payload.message)

    emergency, emergency_reason = detect_emergency(normalized)
    pending_intake = needs_more_information(normalized)

    if pending_intake and not emergency:
        disease, confidence = "Insufficient information", 0.0
    else:
        text_for_model = " ".join(normalized)
        disease, confidence = predict_disease(text_for_model)
    requires_human_verification, human_verification_reason = determine_human_verification(emergency, confidence)

    _triage_meta = triage_agent_decision(normalized, emergency, emergency_reason)

    report = generate_doctor_report_de(
        patient_name=payload.patient_name,
        raw_message=payload.message,
        detected_language=language,
        normalized_symptoms=normalized,
        emergency=emergency,
        emergency_reason=emergency_reason,
        predicted_disease=disease,
        confidence=confidence,
    )

    case_id = insert_case(
        {
            "patient_name": payload.patient_name,
            "raw_message": payload.message,
            "detected_language": language,
            "normalized_symptoms": json.dumps(normalized, ensure_ascii=False),
            "emergency": int(emergency),
            "emergency_reason": emergency_reason,
            "requires_human_verification": int(requires_human_verification),
            "human_verification_reason": human_verification_reason,
            "consent_accepted": int(payload.consent_accepted),
            "predicted_disease": disease,
            "confidence": confidence,
            "doctor_report_de": report,
        }
    )

    return ChatResponse(
        case_id=case_id,
        detected_language=language,
        normalized_symptoms=normalized,
        needs_more_information=pending_intake and not emergency,
        follow_up_prompt=FOLLOW_UP_PROMPTS.get(language, FOLLOW_UP_PROMPTS["en"]) if (pending_intake and not emergency) else "",
        emergency=emergency,
        emergency_reason=emergency_reason,
        requires_human_verification=requires_human_verification,
        human_verification_reason=human_verification_reason,
        predicted_disease=disease,
        confidence=confidence,
        doctor_report_de=report,
        assistant_reply=LANG_REPLY.get(language, LANG_REPLY["en"]),
    )
