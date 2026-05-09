# MediBridge AI - MVP

MVP first features implemented:
- Symptom chat endpoint
- Language support: Arabic, German, English, Turkish
- Emergency detection
- Disease prediction with Scikit-learn
- German doctor report generation
- Simple dashboard summary
- Human verification flag for high-risk/low-confidence cases

## Project Structure

```text
medibridge-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agents/
│   │   ├── ml/
│   │   ├── services/
│   │   ├── database/
│   │   └── schemas/
│   └── requirements.txt
├── frontend/
│   └── react-app/
├── datasets/
├── notebooks/
├── docs/
│   ├── architecture.md
│   └── security.md
├── privacy_policy.md
├── gdpr_notes.md
├── ai_limitations.md
└── risk_management.md
```

## Backend Run

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend docs: `http://127.0.0.1:8000/docs`

## Frontend Run

```bash
cd frontend/react-app
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:5173`

## API Endpoints

- `POST /api/chat`
- `GET /api/dashboard/summary`
- `GET /health`

## Safety & Compliance
- Human Oversight is required for high-risk and low-confidence cases.
- AI outputs are assistive and not final diagnosis.
- Compliance package is included for privacy, GDPR notes, AI limitations, and risk management.
