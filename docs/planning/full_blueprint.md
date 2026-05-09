# MediBridge AI - Full System Blueprint

## 1) Full Architecture Diagram
```mermaid
flowchart TD
    U[Patient/User] --> FE[React App]
    D[Doctor/Admin] --> FE

    FE -->|HTTPS REST| BE[FastAPI Backend]

    subgraph Backend Core
        BE --> AUTH[Auth Service]
        BE --> CHAT[Symptom Chat Service]
        BE --> TRIAGE[Emergency & Risk Triage]
        BE --> AGENTS[CrewAI Orchestrator]
        BE --> ML1[ML Disease Predictor]
        BE --> REP[German Report Generator]
        BE --> LOGS[Audit Logger]
        BE --> CONSENT[Consent & Privacy Service]
    end

    AGENTS --> A1[Triage Agent]
    AGENTS --> A2[Translation Agent]
    AGENTS --> A3[Safety Agent]
    AGENTS --> A4[Doctor Report Agent]
    AGENTS --> A5[Video Recommendation Agent]

    ML1 --> DB[(SQLite now / PostgreSQL prod)]
    LOGS --> DB
    CONSENT --> DB
    TRIAGE --> DB

    RAD[RAG Service - Phase 2] --> VDB[(ChromaDB/FAISS)]
    CHAT --> RAD

    CNN[CNN Imaging Service - Phase 3] --> BE

    FE --> DASH[Dashboard UI]
    DASH -->|/api/dashboard| BE
```

## 2) 6-Month Roadmap
- Month 1: Stabilize MVP, auth, consent, delete API, audit logs.
- Month 2: Improve multilingual normalization, dataset v1, model evaluation baseline.
- Month 3: Introduce RAG medical knowledge retrieval (read-only, cited output).
- Month 4: Deploy PostgreSQL, role-based access, production security hardening.
- Month 5: CNN prototype for image triage (non-diagnostic), calibration and explainability.
- Month 6: Clinical pilot readiness package (DPIA, model cards, incident playbooks, validation report).

## 3) Folder Structure
```text
medibridge-ai/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agents/
│   │   ├── ml/
│   │   ├── services/
│   │   ├── database/
│   │   ├── schemas/
│   │   ├── api/
│   │   └── core/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   └── react-app/
│       ├── src/
│       │   ├── pages/
│       │   ├── components/
│       │   ├── hooks/
│       │   ├── api/
│       │   └── styles/
├── datasets/
├── notebooks/
├── docs/
└── .github/
    └── workflows/
```

## 4) Database Schema (Core)
- users(id, email, password_hash, role, created_at)
- patients(id, external_ref, created_at)
- cases(id, patient_id, raw_message, detected_language, normalized_symptoms_json, emergency, emergency_reason, requires_human_verification, human_verification_reason, predicted_disease, confidence, doctor_report_de, created_at)
- feedback(id, case_id, feedback_type, comment, created_at)
- consents(id, patient_id, consent_version, accepted, accepted_at)
- audit_logs(id, actor_id, action, resource_type, resource_id, metadata_json, created_at)

## 5) Agent List
- Intake Agent: validates completeness, asks follow-up.
- Translation Agent: multilingual normalization/translation.
- Triage Agent: emergency/risk determination.
- Disease Prediction Agent: invokes ML scoring and confidence checks.
- Safety Agent: blocks unsafe outputs, enforces disclaimer.
- Doctor Report Agent: produces German physician summary.
- Video Recommendation Agent (phase 2+): exercises/physio/stress videos.
- Compliance Agent: consent, retention, deletion workflow checks.

## 6) Use Case Diagram
```mermaid
flowchart LR
    P[Patient] --> UC1[Submit Symptoms]
    P --> UC2[Provide Consent]
    P --> UC3[Give Feedback]

    DR[Doctor] --> UC4[Review German Report]
    DR --> UC5[Verify High-Risk Cases]

    AD[Admin] --> UC6[View Dashboard]
    AD --> UC7[Manage Users & Roles]
    AD --> UC8[Run Data Deletion Request]
```

## 7) ERD
```mermaid
erDiagram
    USERS ||--o{ AUDIT_LOGS : creates
    PATIENTS ||--o{ CASES : has
    CASES ||--o{ FEEDBACK : receives
    PATIENTS ||--o{ CONSENTS : signs

    USERS {
      int id
      string email
      string password_hash
      string role
      datetime created_at
    }
    PATIENTS {
      int id
      string external_ref
      datetime created_at
    }
    CASES {
      int id
      int patient_id
      text raw_message
      string detected_language
      text normalized_symptoms_json
      bool emergency
      text emergency_reason
      bool requires_human_verification
      text human_verification_reason
      string predicted_disease
      float confidence
      text doctor_report_de
      datetime created_at
    }
    FEEDBACK {
      int id
      int case_id
      string feedback_type
      text comment
      datetime created_at
    }
    CONSENTS {
      int id
      int patient_id
      string consent_version
      bool accepted
      datetime accepted_at
    }
    AUDIT_LOGS {
      int id
      int actor_id
      string action
      string resource_type
      int resource_id
      text metadata_json
      datetime created_at
    }
```

## 8) Full Tech Stack
- Frontend: React + Vite
- Backend: FastAPI + Pydantic
- Agents: CrewAI
- ML: scikit-learn
- CNN/DL: PyTorch (phase 3)
- DB: SQLite (MVP), PostgreSQL (production)
- Cache/Queue (phase 2): Redis + Celery/RQ
- RAG (phase 2): LangChain or LlamaIndex + ChromaDB/FAISS
- Observability: structured logs + Prometheus/Grafana (phase 3)
- Security: JWT, bcrypt, RBAC, HTTPS via reverse proxy

## 9) ML Training Plan
- Data sources: symptom-condition datasets + curated multilingual mappings.
- Preprocessing: normalization, tokenization, language-aware cleaning.
- Baselines: LogisticRegression, LinearSVC, XGBoost-light.
- Metrics: macro F1, recall for emergency-related classes, calibration error.
- Validation: stratified split + cross-validation + error analysis slices by language.
- Safety gates: min recall threshold for critical classes before release.

## 10) CNN Training Plan
- Scope: image triage assistance only (non-final diagnosis).
- Data: de-identified public datasets with documented licenses.
- Model: EfficientNet/ResNet baseline + Grad-CAM explainability.
- Metrics: sensitivity, specificity, AUROC, subgroup bias checks.
- Clinical safeguards: mandatory human review; no autonomous decision.

## 11) Prompt Engineering Guidelines
- System prompt: "AI assistant with human oversight, never autonomous diagnosis."
- Output policy: neutral, non-prescriptive medication language.
- Mandatory fields: confidence, limitations, follow-up advice, disclaimer.
- Guardrails: unsafe medical instructions blocked by Safety Agent.

## 12) Backend APIs (Target)
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/chat`
- `GET /api/cases/{id}`
- `POST /api/feedback`
- `GET /api/dashboard/summary`
- `DELETE /api/cases/{id}` (GDPR erase)
- `GET /health`

## 13) React UI Plan
- Pages: Login, Symptom Chat, Case Detail, Dashboard, Admin.
- Components: MessageBox, RiskBadge, ReportPanel, FeedbackButtons, ConsentModal.
- UX rules: simple language, clear emergency escalation, always visible disclaimer.

## 14) Dashboard Scope
- KPIs: total cases, emergency count, verification pending count, language distribution.
- Quality: model confidence distribution, feedback quality trends.
- Compliance: consent rate, deletion requests, audit-log events per day.

## 15) Professional GitHub Plan
- Branch model: `main`, `develop`, `feature/*`, `hotfix/*`.
- PR policy: template + required reviews + CI checks.
- CI: lint, tests, type checks, security scan.
- Versioning: Semantic Versioning + release notes.
- Project management: GitHub Projects milestones aligned to 6-month roadmap.
