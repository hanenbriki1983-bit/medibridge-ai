from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    patient_name: str | None = None
    message: str = Field(min_length=3)
    consent_accepted: bool = Field(
        default=False,
        description="User consent must be accepted before symptom processing.",
    )


class ChatResponse(BaseModel):
    case_id: int
    detected_language: str
    normalized_symptoms: list[str]
    needs_more_information: bool
    follow_up_prompt: str
    emergency: bool
    emergency_reason: str
    requires_human_verification: bool
    human_verification_reason: str
    predicted_disease: str
    confidence: float
    doctor_report_de: str
    assistant_reply: str
