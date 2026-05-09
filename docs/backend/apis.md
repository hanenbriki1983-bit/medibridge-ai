# Backend API Specification (MVP+)

## Auth
- POST `/api/auth/register`
- POST `/api/auth/login`

## Clinical
- POST `/api/chat`
  - Input: `patient_name`, `message`
  - Output: language, normalized symptoms, emergency flags, human verification flags, disease prediction, report de

- GET `/api/cases/{id}`
  - Returns stored case

## Feedback
- POST `/api/feedback`
  - feedback_type: `helpful | inaccurate | bad_translation`

## Dashboard
- GET `/api/dashboard/summary`

## Privacy
- DELETE `/api/cases/{id}`
  - GDPR erase request

## Health
- GET `/health`
