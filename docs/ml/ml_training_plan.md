# ML Training Plan (Symptoms -> Disease)

## Objective
Predict probable disease class from normalized symptoms with uncertainty scoring.

## Data Strategy
- Start with curated multilingual symptom-condition examples.
- Add real anonymized feedback-based corrections.
- Keep strict train/validation/test split.

## Pipeline
- Normalize symptoms
- Vectorization (BoW/TF-IDF)
- Baseline models (LogReg, SVM)
- Confidence calibration

## Evaluation
- Macro F1
- Recall for critical classes
- Per-language performance slices

## Release Policy
- Model release only if critical-class recall passes threshold.
- Low-confidence outputs require human verification.
