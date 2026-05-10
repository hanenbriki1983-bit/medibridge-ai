import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"
LANGUAGES = ["auto", "en", "de", "ar", "tr", "fr", "el", "ru"]


def post_chat(payload: dict) -> dict:
    response = requests.post(f"{API_BASE_URL}/api/chat", json=payload, timeout=20)
    response.raise_for_status()
    return response.json()


def analyze_xray_file(file_obj) -> dict:
    files = {"file": (file_obj.name, file_obj.getvalue(), file_obj.type or "application/octet-stream")}
    response = requests.post(f"{API_BASE_URL}/api/xray/analyze", files=files, timeout=60)
    response.raise_for_status()
    return response.json()


def get_dashboard() -> dict:
    response = requests.get(f"{API_BASE_URL}/api/dashboard/summary", timeout=20)
    response.raise_for_status()
    return response.json()


def check_backend_health() -> tuple[bool, str]:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        response.raise_for_status()
        return True, "Connected"
    except requests.RequestException as exc:
        return False, str(exc)


st.set_page_config(page_title="MediBridge AI", page_icon=":hospital:", layout="wide")
st.title("MediBridge AI")
st.caption("Clinical triage assistant demo. For awareness only, not a final diagnosis.")
healthy, message = check_backend_health()

if healthy:
    st.success("Backend Connected")
else:
    st.error(f"Backend Error: {message}")

with st.sidebar:
    st.subheader("Backend")
    st.write(f"API URL: `{API_BASE_URL}`")
    st.write(f"Status: {'Connected' if healthy else 'Disconnected'}")
    patient_name = st.text_input("Patient name (optional)")
    language = st.selectbox("Preferred language", LANGUAGES, index=0)
    xray_file = st.file_uploader("Attach X-ray image (optional)", type=["png", "jpg", "jpeg"])
    xray_note = st.text_area("X-ray note (optional)", placeholder="e.g., persistent cough for 10 days")
    consent = st.checkbox("I accept consent for clinical processing.")
    if st.button("Clear Chat"):
        st.session_state["chat_history"] = []
        st.session_state["last_result"] = None
    if st.button("Refresh Dashboard"):
        st.session_state["refresh_dashboard"] = True

col1, col2 = st.columns([3, 2])

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None
if "last_xray_result" not in st.session_state:
    st.session_state["last_xray_result"] = None

with col1:
    st.subheader("Symptom Chatbot")
    st.caption("Write your symptoms below and press Enter.")

    for item in st.session_state["chat_history"]:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])

    user_text = st.chat_input("Describe your symptoms...")
    if user_text:
        st.session_state["chat_history"].append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        if not consent:
            error_text = "Consent is required. Please enable consent in the sidebar."
            st.session_state["chat_history"].append({"role": "assistant", "content": error_text})
            with st.chat_message("assistant"):
                st.error(error_text)
        else:
            preferred_language = None if language == "auto" else language
            payload = {
                "patient_name": patient_name or None,
                "message": user_text.strip(),
                "preferred_language": preferred_language,
                "consent_accepted": consent,
                "xray_attached": xray_file is not None,
                "xray_note": xray_note.strip() if xray_note.strip() else None,
            }
            try:
                result = post_chat(payload)
                st.session_state["last_result"] = result

                assistant_text = result.get("assistant_reply", "No assistant reply returned.")
                st.session_state["chat_history"].append({"role": "assistant", "content": assistant_text})
                with st.chat_message("assistant"):
                    st.markdown(assistant_text)
                    if result.get("xray_guidance"):
                        st.info(result["xray_guidance"])
                    if result.get("follow_up_prompt"):
                        st.info(result["follow_up_prompt"])
                    if result.get("nutrition_tips"):
                        st.markdown("**Nutrition tips**")
                        for tip in result["nutrition_tips"]:
                            st.write(f"- {tip}")
                    if result.get("exercise_tips"):
                        st.markdown("**Exercise tips**")
                        for tip in result["exercise_tips"]:
                            st.write(f"- {tip}")
            except requests.HTTPError as exc:
                try:
                    detail = exc.response.json()
                except Exception:
                    detail = exc.response.text
                err = f"Request failed: {detail}"
                st.session_state["chat_history"].append({"role": "assistant", "content": err})
                with st.chat_message("assistant"):
                    st.error(err)
            except requests.RequestException as exc:
                err = f"Backend unavailable: {exc}"
                st.session_state["chat_history"].append({"role": "assistant", "content": err})
                with st.chat_message("assistant"):
                    st.error(err)

    st.markdown("### X-ray Analysis")
    if xray_file is not None:
        st.image(xray_file, caption="Uploaded X-ray image", use_container_width=True)
        if st.button("Analyze X-ray"):
            try:
                xray_result = analyze_xray_file(xray_file)
                st.session_state["last_xray_result"] = xray_result
            except requests.HTTPError as exc:
                st.error(f"X-ray request failed: {exc.response.text}")
            except requests.RequestException as exc:
                st.error(f"X-ray service unavailable: {exc}")
    else:
        st.caption("Upload an X-ray in the sidebar to enable analysis.")

    if st.session_state["last_xray_result"]:
        xr = st.session_state["last_xray_result"]
        st.write(f"Model available: `{xr.get('model_available')}`")
        st.write(f"Predicted class: `{xr.get('predicted_class')}`")
        st.write(f"Confidence: `{xr.get('confidence')}`")
        st.write(f"Needs human verification: `{xr.get('requires_human_verification')}`")
        st.info(xr.get("message", ""))

    if st.session_state["last_result"]:
        result = st.session_state["last_result"]
        st.markdown("### Last Case Details")
        st.write(f"Case ID: `{result['case_id']}`")
        st.write(f"Detected language: `{result['detected_language']}`")
        st.write(f"Predicted disease: `{result['predicted_disease']}`")
        st.write(f"Confidence: `{result['confidence']:.2f}`")
        st.write(f"Emergency: `{result['emergency']}`")
        st.write(f"Needs human verification: `{result['requires_human_verification']}`")
        if result.get("xray_guidance"):
            st.write(f"X-ray guidance: {result['xray_guidance']}")
        st.text_area("Doctor report (DE)", value=result.get("doctor_report_de", ""), height=180, disabled=True)

with col2:
    st.subheader("Dashboard Summary")
    try:
        summary = get_dashboard()
        st.metric("Total Cases", summary["total_cases"])
        st.metric("Emergency Cases", summary["emergency_cases"])

        st.markdown("Top Predicted Diseases")
        if summary["top_predicted_diseases"]:
            st.table(summary["top_predicted_diseases"])
        else:
            st.write("No data yet.")

        st.markdown("Language Distribution")
        if summary["language_distribution"]:
            st.table(summary["language_distribution"])
        else:
            st.write("No data yet.")
    except requests.RequestException as exc:
        st.warning(f"Could not load dashboard: {exc}")
