from pydantic import BaseModel


class DeleteCaseResponse(BaseModel):
    deleted: bool
    case_id: int


class ReviewQueueItem(BaseModel):
    case_id: int
    patient_name: str | None
    detected_language: str
    predicted_disease: str
    confidence: float
    emergency: bool
    human_verification_reason: str
    created_at: str


class ReviewQueueResponse(BaseModel):
    pending_count: int
    items: list[ReviewQueueItem]
