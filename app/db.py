from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "medibridge.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT,
                raw_symptoms TEXT NOT NULL,
                detected_language TEXT NOT NULL,
                normalized_symptoms TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                risk_reason TEXT NOT NULL,
                predicted_condition TEXT NOT NULL,
                prediction_confidence REAL NOT NULL,
                doctor_report_de TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def save_case(payload: dict[str, object]) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO cases (
                patient_name,
                raw_symptoms,
                detected_language,
                normalized_symptoms,
                risk_level,
                risk_reason,
                predicted_condition,
                prediction_confidence,
                doctor_report_de
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.get("patient_name"),
                payload["raw_symptoms"],
                payload["detected_language"],
                payload["normalized_symptoms"],
                payload["risk_level"],
                payload["risk_reason"],
                payload["predicted_condition"],
                payload["prediction_confidence"],
                payload["doctor_report_de"],
            ),
        )
        return int(cur.lastrowid)
