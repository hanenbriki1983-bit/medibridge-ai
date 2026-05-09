import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000/api";

export default function App() {
  const [message, setMessage] = useState("");
  const [patientName, setPatientName] = useState("");
  const [consentAccepted, setConsentAccepted] = useState(false);
  const [result, setResult] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [reviewQueue, setReviewQueue] = useState(null);
  const [deleteCaseId, setDeleteCaseId] = useState("");
  const [deleteStatus, setDeleteStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const submitSymptoms = async (event) => {
    event.preventDefault();
    if (!consentAccepted) {
      setDeleteStatus("Consent is required before using the clinical assistant.");
      return;
    }

    setLoading(true);
    setDeleteStatus("");
    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_name: patientName || null,
          message,
          consent_accepted: consentAccepted,
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setDeleteStatus(data.detail || "Request failed.");
        return;
      }
      setResult(data);
      setMessage("");
    } finally {
      setLoading(false);
    }
  };

  const loadDashboard = async () => {
    const res = await fetch(`${API_BASE}/dashboard/summary`);
    const data = await res.json();
    setDashboard(data);
  };

  const loadReviewQueue = async () => {
    const res = await fetch(`${API_BASE}/compliance/review-queue`);
    const data = await res.json();
    setReviewQueue(data);
  };

  const deleteCase = async () => {
    if (!deleteCaseId.trim()) {
      setDeleteStatus("Enter a case ID.");
      return;
    }
    const res = await fetch(`${API_BASE}/compliance/cases/${deleteCaseId}`, {
      method: "DELETE",
    });
    const data = await res.json();
    if (!res.ok) {
      setDeleteStatus(data.detail || "Delete failed.");
      return;
    }
    setDeleteStatus(`Case ${data.case_id} deleted successfully.`);
    setDeleteCaseId("");
    loadReviewQueue();
    loadDashboard();
  };

  return (
    <main className="page">
      <h1>MediBridge AI MVP</h1>
      <section className="card">
        <h2>تنبيه مهم</h2>
        <p>
          أنا مساعد صحي ذكي، أقدم معلومات عامة وأساعدك على فهم أعراضك، لكنني لست
          بديلاً عن الطبيب.
        </p>
      </section>

      <section className="card">
        <h2>Symptom Chat</h2>
        <form onSubmit={submitSymptoms}>
          <input
            placeholder="Patient name (optional)"
            value={patientName}
            onChange={(e) => setPatientName(e.target.value)}
          />
          <textarea
            placeholder="Write symptoms in Arabic, German, English, Turkish, Russian, Greek, or French"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />
          <label>
            <input
              type="checkbox"
              checked={consentAccepted}
              onChange={(e) => setConsentAccepted(e.target.checked)}
            />
            I consent to processing my health-related input for triage support.
          </label>
          <button type="submit" disabled={loading}>{loading ? "Analyzing..." : "Analyze"}</button>
        </form>
      </section>

      {result && (
        <section className="card">
          <h2>Result</h2>
          <p><strong>Language:</strong> {result.detected_language}</p>
          <p><strong>Emergency:</strong> {String(result.emergency)}</p>
          <p><strong>Needs human verification:</strong> {String(result.requires_human_verification)}</p>
          <p><strong>Reason:</strong> {result.human_verification_reason}</p>
          <p><strong>Disease prediction:</strong> {result.predicted_disease} ({result.confidence})</p>
          <p><strong>Assistant reply:</strong> {result.assistant_reply}</p>
          <p>
            <strong>تنبيه:</strong> هذه المعلومات للتوعية فقط، استشر طبيباً مختصاً
            في الحالات الخطيرة.
          </p>
          <pre>{result.doctor_report_de}</pre>
        </section>
      )}

      <section className="card">
        <h2>Dashboard</h2>
        <button onClick={loadDashboard}>Refresh Dashboard</button>
        {dashboard && (
          <div>
            <p><strong>Total cases:</strong> {dashboard.total_cases}</p>
            <p><strong>Emergency cases:</strong> {dashboard.emergency_cases}</p>
            <p><strong>Top diseases:</strong> {dashboard.top_predicted_diseases.map((x) => `${x.disease} (${x.count})`).join(", ") || "-"}</p>
            <p><strong>Languages:</strong> {dashboard.language_distribution.map((x) => `${x.language} (${x.count})`).join(", ") || "-"}</p>
          </div>
        )}
      </section>

      <section className="card">
        <h2>Clinician Review Queue</h2>
        <button onClick={loadReviewQueue}>Load Review Queue</button>
        {reviewQueue && (
          <div>
            <p><strong>Pending cases:</strong> {reviewQueue.pending_count}</p>
            {reviewQueue.items.length === 0 ? (
              <p>No pending high-risk cases.</p>
            ) : (
              reviewQueue.items.map((item) => (
                <p key={item.case_id}>
                  #{item.case_id} | {item.predicted_disease} | conf {item.confidence} | reason: {item.human_verification_reason}
                </p>
              ))
            )}
          </div>
        )}
      </section>

      <section className="card">
        <h2>GDPR Data Deletion</h2>
        <input
          placeholder="Case ID"
          value={deleteCaseId}
          onChange={(e) => setDeleteCaseId(e.target.value)}
        />
        <button onClick={deleteCase}>Delete Case</button>
        {deleteStatus && <p>{deleteStatus}</p>}
      </section>
    </main>
  );
}
