import streamlit as st
from PIL import Image
import ai_engine
import config
import calculators
import medical_data


# ------------------------------------------------
#   PAGE SETTINGS
# ------------------------------------------------
st.set_page_config(
    page_title="Health Checker 365",
    page_icon="🏥",
    layout="wide"
)

# Global style override (PROFESSIONAL, HIGH VISIBILITY)
st.markdown("""
    <style>
        body { background-color: #F8FAFC; }
        .main-title { color: #0F172A; font-size: 32px; font-weight: 900; }
        .section-title { color: #1E293B; font-size: 24px; font-weight: 700; margin-top: 20px; }
        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            color: #0F172A;
        }
        .clinical-card { border-left: 6px solid #0EA5E9; }
        .patient-card { border-left: 6px solid #10B981; }
    </style>
""", unsafe_allow_html=True)


# ------------------------------------------------
#   SIDEBAR
# ------------------------------------------------
with st.sidebar:
    st.title("🏥 Health Checker 365")
    st.write("AI-powered clinical & patient-friendly medical support.")

    if not config.GEMINI_API_KEY:
        st.error("⚠️ Missing Gemini API Key in config.py")

    menu = st.radio(
        "Select Module:",
        [
            "💬 Chat & Diagnosis",
            "💊 Drug Monograph",
            "🧮 Medical Calculators",
            "📸 Image Diagnosis"
        ]
    )


# ========================================================
# 1️⃣ CHAT & DIAGNOSIS
# ========================================================
if menu == "💬 Chat & Diagnosis":

    st.markdown("<div class='main-title'>💬 AI Clinical Chat</div>", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["text"])

    if user_input := st.chat_input("Describe symptoms or ask a medical question..."):

        st.session_state.chat_history.append({"role": "user", "text": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing clinically..."):
                response = ai_engine.get_hybrid_response(user_input)

            # SPLIT INTO TWO CARD SECTIONS
            st.markdown("<div class='section-title'>🩺 Diagnosis Result</div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            if "### 👨‍⚕️ Clinical View" in response:
                clinical = response.split("### 👨‍⚕️ Clinical View")[1].split("### 🏡 Patient View")[0]
                patient = response.split("### 🏡 Patient View")[1]

                with col1:
                    st.markdown("<div class='card clinical-card'>", unsafe_allow_html=True)
                    st.markdown("### 👨‍⚕️ Clinical View")
                    st.markdown(clinical)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='card patient-card'>", unsafe_allow_html=True)
                    st.markdown("### 🏡 Patient View")
                    st.markdown(patient)
                    st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.write(response)

        st.session_state.chat_history.append({"role": "assistant", "text": response})


# ========================================================
# 2️⃣ DRUG MODULE
# ========================================================
elif menu == "💊 Drug Monograph":

    st.markdown("<div class='main-title'>💊 Drug Monograph</div>", unsafe_allow_html=True)

    drug = st.text_input("Enter Drug Name")

    if st.button("Search"):

        internal_data = medical_data.get_drug_data(drug)

        with st.spinner("Generating monograph..."):
            output = ai_engine.get_hybrid_response(
                f"Generate dual-view monograph for {drug}",
                context_data=internal_data
            )

        col1, col2 = st.columns(2)

        clinical = output.split("### 👨‍⚕️ Clinical View")[1].split("### 🏡 Patient View")[0]
        patient = output.split("### 🏡 Patient View")[1]

        with col1:
            st.markdown("<div class='card clinical-card'>", unsafe_allow_html=True)
            st.markdown("### 👨‍⚕️ Clinical View")
            st.markdown(clinical)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card patient-card'>", unsafe_allow_html=True)
            st.markdown("### 🏡 Patient View")
            st.markdown(patient)
            st.markdown("</div>", unsafe_allow_html=True)


# ========================================================
# 3️⃣ CALCULATORS
# ========================================================
elif menu == "🧮 Medical Calculators":

    st.markdown("<div class='main-title'>🧮 Medical Calculators</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["BMI", "eGFR"])

    # BMI
    with tab1:
        st.markdown("<div class='section-title'>BMI Calculator</div>", unsafe_allow_html=True)
        w = st.number_input("Weight (kg)", 10.0)
        h = st.number_input("Height (cm)", 50.0)

        if st.button("Calculate BMI"):
            val, cat = calculators.calc_bmi(w, h)
            st.success(f"BMI: {val} — {cat}")

    # eGFR
    with tab2:
        st.markdown("<div class='section-title'>eGFR Calculator</div>", unsafe_allow_html=True)
        s = st.number_input("Serum Creatinine (mg/dL)", 0.1)
        age = st.number_input("Age", 1)
        gender = st.selectbox("Gender", ["Male", "Female"])

        if st.button("Calculate eGFR"):
            egfr = calculators.calc_egfr(s, age, gender)
            st.success(f"Estimated GFR: {egfr} mL/min")


# ========================================================
# 4️⃣ IMAGE ANALYSIS
# ========================================================
elif menu == "📸 Image Diagnosis":

    st.markdown("<div class='main-title'>📸 Medical Image Diagnosis</div>", unsafe_allow_html=True)

    upload = st.file_uploader("Upload X-ray / Skin lesion / Scan", type=["jpg", "png", "jpeg"])

    if upload:
        img = Image.open(upload)
        st.image(img, width=350)

        if st.button("Analyze Image"):

            with st.spinner("Analyzing medically..."):
                result = ai_engine.get_hybrid_response(
                    "Analyze this medical image and give findings.",
                    image=img
                )

            col1, col2 = st.columns(2)

            clinical = result.split("### 👨‍⚕️ Clinical View")[1].split("### 🏡 Patient View")[0]
            patient = result.split("### 🏡 Patient View")[1]

            with col1:
                st.markdown("<div class='card clinical-card'>", unsafe_allow_html=True)
                st.markdown("### 👨‍⚕️ Clinical View")
                st.markdown(clinical)
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='card patient-card'>", unsafe_allow_html=True)
                st.markdown("### 🏡 Patient View")
                st.markdown(patient)
                st.markdown("</div>", unsafe_allow_html=True)
