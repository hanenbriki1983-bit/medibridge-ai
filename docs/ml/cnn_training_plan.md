# CNN Training Plan (Imaging Phase)

## Scope
Assistive image triage only; no autonomous diagnosis.

## Data
- Public de-identified medical image datasets.
- License and provenance documentation mandatory.

## Model Flow
- Preprocessing
- Transfer learning (EfficientNet/ResNet)
- Validation and calibration
- Explainability maps (Grad-CAM)

## Risk Controls
- Mandatory clinician review for all outputs.
- Bias/performance checks across subgroups.
- No treatment advice directly from CNN output.
