from pydantic import BaseModel, Field


class IntakeRequest(BaseModel):
    patient_name: str | None = Field(default=None, description="Optional patient display name")
    symptoms_text: str = Field(min_length=3, description="Raw user symptom input")


class IntakeResponse(BaseModel):
    case_id: int
    detected_language: str
    normalized_symptoms: list[str]
    risk_level: str
    risk_reason: str
    predicted_condition: str
    prediction_confidence: float
    doctor_report_de: str
