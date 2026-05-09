# AI Limitations

## Scope Limits
- This system provides preliminary triage support only.
- It is not a diagnostic replacement for physicians.

## Model Limits
- MVP model uses small curated training samples.
- Probabilities may be unstable for rare symptom combinations.
- Language nuance and colloquial phrasing can reduce accuracy.

## Clinical Limits
- No full patient history, lab values, imaging, or medication interactions.
- Emergency rules are simplified and may miss atypical presentations.

## Failure Modes
- False negatives in emergency detection for uncommon phrasing.
- False positives causing unnecessary escalation.
- Overconfidence when symptom normalization is incomplete.

## Mitigations
- Mandatory human verification for high-risk and low-confidence outputs.
- Explicit confidence and reason outputs.
- Continuous dataset expansion and clinical validation loops.

## Explainable AI Commitments
- Show normalized symptoms.
- Show emergency trigger reason.
- Show model confidence.
- Keep inference logs for audit.
