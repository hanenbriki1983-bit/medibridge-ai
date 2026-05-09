from fastapi import APIRouter, HTTPException

from app.database.db import delete_case, get_review_queue
from app.schemas.compliance import DeleteCaseResponse, ReviewQueueItem, ReviewQueueResponse

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/review-queue", response_model=ReviewQueueResponse)
def review_queue() -> ReviewQueueResponse:
    items = get_review_queue(limit=50)
    return ReviewQueueResponse(
        pending_count=len(items),
        items=[ReviewQueueItem(**item) for item in items],
    )


@router.delete("/cases/{case_id}", response_model=DeleteCaseResponse)
def erase_case(case_id: int) -> DeleteCaseResponse:
    deleted = delete_case(case_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Case not found")
    return DeleteCaseResponse(deleted=True, case_id=case_id)
