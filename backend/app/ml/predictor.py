from pathlib import Path
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_PATH = Path(__file__).resolve().parent / "disease_model.joblib"

TRAINING_SAMPLES = [
    ("fever cough sore throat", "Acute Respiratory Infection"),
    ("fieber husten halsschmerzen", "Acute Respiratory Infection"),
    ("حمى سعال ألم حلق", "Acute Respiratory Infection"),
    ("ates oksuruk bogaz agrisi", "Acute Respiratory Infection"),
    ("nausea vomiting diarrhea abdominal pain", "Gastroenteritis"),
    ("ubelkeit erbrechen durchfall bauchschmerzen", "Gastroenteritis"),
    ("غثيان قيء إسهال ألم بطن", "Gastroenteritis"),
    ("mide bulantisi kusma ishal karin agrisi", "Gastroenteritis"),
    ("headache nausea", "Migraine"),
    ("kopfschmerzen ubelkeit", "Migraine"),
    ("صداع غثيان", "Migraine"),
    ("bas agrisi mide bulantisi", "Migraine"),
    ("chest pain shortness of breath", "Cardiopulmonary Emergency"),
    ("brustschmerzen atemnot", "Cardiopulmonary Emergency"),
    ("ألم صدر ضيق تنفس", "Cardiopulmonary Emergency"),
    ("gogus agrisi nefes darligi", "Cardiopulmonary Emergency"),
]


def _train_pipeline() -> Pipeline:
    x_train = [text for text, _ in TRAINING_SAMPLES]
    y_train = [label for _, label in TRAINING_SAMPLES]

    model = Pipeline(
        steps=[
            ("vectorizer", CountVectorizer(ngram_range=(1, 2))),
            ("classifier", LogisticRegression(max_iter=1000)),
        ]
    )
    model.fit(x_train, y_train)
    return model


def get_model() -> Pipeline:
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)

    model = _train_pipeline()
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def predict_disease(text_for_model: str) -> tuple[str, float]:
    model = get_model()
    proba = model.predict_proba([text_for_model])[0]
    idx = int(proba.argmax())
    return str(model.classes_[idx]), float(round(proba[idx], 2))
