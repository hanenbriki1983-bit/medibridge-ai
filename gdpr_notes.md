# GDPR Notes

## Roles
- Data Controller: deploying healthcare organization
- Data Processor: platform/operator managing infrastructure

## GDPR-Relevant Requirements
1. Records of Processing Activities (RoPA)
2. Data Protection Impact Assessment (DPIA) for medical-risk processing
3. Explicit policy for consent/legal basis
4. Data subject rights workflow (access, erase, rectify)
5. Breach notification procedure

## Technical Mapping in MediBridge AI
- Human oversight flags on high-risk outputs
- Explainability artifacts: symptoms, emergency reason, model confidence
- Auditability through structured logs and case storage

## Data Deletion Mechanism (Required)
- Provide endpoint or admin tool to delete a case by `case_id`.
- Log deletion request metadata (who/when/why) without re-exposing deleted health content.
- Ensure deletion in backups follows retention policy.

## International Transfer
- If cloud region is outside EU, SCCs and transfer impact assessments are required.

## Open Items Before Production
- Complete DPIA
- Appoint DPO/contact
- Implement retention schedule automation
- Add signed confidentiality and access governance policies
