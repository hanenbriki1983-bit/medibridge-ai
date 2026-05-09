from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parents[2] / "medibridge.db"


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
                raw_message TEXT NOT NULL,
                detected_language TEXT NOT NULL,
                normalized_symptoms TEXT NOT NULL,
                emergency INTEGER NOT NULL,
                emergency_reason TEXT NOT NULL,
                requires_human_verification INTEGER NOT NULL DEFAULT 0,
                human_verification_reason TEXT NOT NULL DEFAULT '',
                consent_accepted INTEGER NOT NULL DEFAULT 0,
                predicted_disease TEXT NOT NULL,
                confidence REAL NOT NULL,
                doctor_report_de TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        existing_columns = {row["name"] for row in conn.execute("PRAGMA table_info(cases)").fetchall()}
        if "requires_human_verification" not in existing_columns:
            conn.execute(
                "ALTER TABLE cases ADD COLUMN requires_human_verification INTEGER NOT NULL DEFAULT 0"
            )
        if "human_verification_reason" not in existing_columns:
            conn.execute(
                "ALTER TABLE cases ADD COLUMN human_verification_reason TEXT NOT NULL DEFAULT ''"
            )
        if "consent_accepted" not in existing_columns:
            conn.execute(
                "ALTER TABLE cases ADD COLUMN consent_accepted INTEGER NOT NULL DEFAULT 0"
            )


def insert_case(data: dict[str, object]) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO cases (
                patient_name, raw_message, detected_language, normalized_symptoms,
                emergency, emergency_reason, requires_human_verification, human_verification_reason,
                consent_accepted, predicted_disease, confidence, doctor_report_de
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("patient_name"),
                data["raw_message"],
                data["detected_language"],
                data["normalized_symptoms"],
                data["emergency"],
                data["emergency_reason"],
                data["requires_human_verification"],
                data["human_verification_reason"],
                data["consent_accepted"],
                data["predicted_disease"],
                data["confidence"],
                data["doctor_report_de"],
            ),
        )
        return int(cursor.lastrowid)


def delete_case(case_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM cases WHERE id = ?", (case_id,))
        return cursor.rowcount > 0


def get_review_queue(limit: int = 50) -> list[dict[str, object]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, patient_name, detected_language, predicted_disease, confidence,
                   emergency, human_verification_reason, created_at
            FROM cases
            WHERE requires_human_verification = 1
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "case_id": int(row["id"]),
            "patient_name": row["patient_name"],
            "detected_language": row["detected_language"],
            "predicted_disease": row["predicted_disease"],
            "confidence": float(row["confidence"]),
            "emergency": bool(row["emergency"]),
            "human_verification_reason": row["human_verification_reason"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def get_dashboard_summary() -> dict[str, object]:
    with get_connection() as conn:
        total_cases = conn.execute("SELECT COUNT(*) AS c FROM cases").fetchone()["c"]
        emergency_cases = conn.execute("SELECT COUNT(*) AS c FROM cases WHERE emergency = 1").fetchone()["c"]

        diseases = conn.execute(
            """
            SELECT predicted_disease, COUNT(*) AS c
            FROM cases
            GROUP BY predicted_disease
            ORDER BY c DESC
            LIMIT 5
            """
        ).fetchall()

        langs = conn.execute(
            """
            SELECT detected_language, COUNT(*) AS c
            FROM cases
            GROUP BY detected_language
            ORDER BY c DESC
            """
        ).fetchall()

    return {
        "total_cases": int(total_cases),
        "emergency_cases": int(emergency_cases),
        "top_predicted_diseases": [{"disease": row["predicted_disease"], "count": int(row["c"])} for row in diseases],
        "language_distribution": [{"language": row["detected_language"], "count": int(row["c"])} for row in langs],
    }
