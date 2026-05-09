from __future__ import annotations

import json

from fastapi import FastAPI

from .db import init_db, save_case
from .schemas import IntakeRequest, IntakeResponse
from .services.disease_model import predict_condition
from .services.language import detect_language
from .services.normalization import normalize_symptoms
from .services.reporting import build_doctor_report_de
from .services.risk_agent import assess_risk

app = FastAPI(title="MediBridge AI MVP", version="0.1.0")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/intake", response_model=IntakeResponse)
def intake(payload: IntakeRequest) -> IntakeResponse:
    detected_language = detect_language(payload.symptoms_text)
    normalized_symptoms = normalize_symptoms(payload.symptoms_text)
    risk_level, risk_reason = assess_risk(normalized_symptoms)
    predicted_condition, prediction_confidence = predict_condition(normalized_symptoms)

    doctor_report_de = build_doctor_report_de(
        patient_name=payload.patient_name,
        raw_text=payload.symptoms_text,
        detected_language=detected_language,
        normalized_symptoms=normalized_symptoms,
        risk_level=risk_level,
        risk_reason=risk_reason,
        predicted_condition=predicted_condition,
        prediction_confidence=prediction_confidence,
    )

    case_id = save_case(
        {
            "patient_name": payload.patient_name,
            "raw_symptoms": payload.symptoms_text,
            "detected_language": detected_language,
            "normalized_symptoms": json.dumps(normalized_symptoms, ensure_ascii=False),
            "risk_level": risk_level,
            "risk_reason": risk_reason,
            "predicted_condition": predicted_condition,
            "prediction_confidence": prediction_confidence,
            "doctor_report_de": doctor_report_de,
        }
    )

    return IntakeResponse(
        case_id=case_id,
        detected_language=detected_language,
        normalized_symptoms=normalized_symptoms,
        risk_level=risk_level,
        risk_reason=risk_reason,
        predicted_condition=predicted_condition,
        prediction_confidence=prediction_confidence,
        doctor_report_de=doctor_report_de,
    )
