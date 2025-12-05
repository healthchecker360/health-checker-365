import streamlit as st
import config
import ai_engine
import medical_data
import calculators
import drug_interactions
import lab
from PIL import Image
import json
import pandas as pd
import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
body {background-color: #F8F9FA; color: #212121; font-family: 'Arial', sans-serif;}
h1, h2, h3, h4 {color: #00796B; font-weight: bold;}
.stButton>button {background-color: #00796B; color: white; border-radius: 10px; padding: 8px 16px; border: none;}
.stButton>button:hover {background-color: #004D40; color: white;}
.stSidebar {background-color: #E0F2F1; padding: 20px;}
.stTextInput>div>div>input, .stNumberInput>div>div>input {border-radius: 8px; border: 1px solid #B0BEC5; padding: 6px;}
.card {background-color: #FFFFFF; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏥 Health Checker 365")
    st.write("AI Medical Assistant")
    if not config.GEMINI_API_KEY:
        st.error("⚠️ API Key missing!")

    menu = st.radio(
        "Modules",
        ["💬 Chat & Diagnosis", "💊 Drug Module", "💉 Drug Interactions",
         "🧮 Calculators", "📊 Lab Interpretation", "📸 Image Analysis"]
    )

# ========================
# 1. Chat & Diagnosis
# ========================
if menu == "💬 Chat & Diagnosis":
    st.header("💬 AI Clinical Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Describe symptoms or medical query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI analyzing..."):
                res = ai_engine.get_hybrid_response(prompt)
                st.expander("👨‍⚕️ Clinical View").markdown(res)
                st.expander("🏡 Patient View").markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# ========================
# 2. Drug Module
# ========================
elif menu == "💊 Drug Module":
    st.header("💊 Drug Information")
    drug = st.text_input("Enter Drug Name:")
    if st.button("Search Drug"):
        internal_data = medical_data.get_drug_data(drug)
        if internal_data:
            st.success("✅ Found in Internal BNF Database")
        else:
            st.warning("⚠️ Not found internally. Fetching AI monograph...")

        with st.spinner("Generating monograph..."):
            res = ai_engine.get_hybrid_response(f"Provide dual-view monograph for {drug}.",
                                                context_data=internal_data)
            st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)

# ========================
# 3. Drug Interactions
# ========================
elif menu == "💉 Drug Interactions":
    st.header("⚠️ Drug Interaction Checker")
    drugs_input = st.text_area("Enter drugs separated by commas:", placeholder="warfarin, amoxicillin")
    if st.button("Check Interactions"):
        drug_list = [d.strip() for d in drugs_input.split(",") if d.strip()]
        interactions = drug_interactions.check_interactions(drug_list)
        if interactions:
            for inter in interactions:
                st.markdown(
                    f"<div class='card'>**{inter['drug1'].title()} + {inter['drug2'].title()}** → {inter['severity']}<br>{inter['note']}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.success("No known interactions found.")

# ========================
# 4. Calculators
# ========================
elif menu == "🧮 Calculators":
    st.header("🧮 Medical Calculators")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("BMI Calculator")
        weight = st.number_input("Weight (kg):", 70.0, key="bmi_w")
        height = st.number_input("Height (cm):", 175.0, key="bmi_h")
        if st.button("Calculate BMI"):
            val, cat = calculators.calc_bmi(weight, height)
            st.markdown(f"<div class='card'><b>BMI:</b> {val} <br><b>Category:</b> {cat}</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("eGFR Calculator")
        creatinine = st.number_input("Serum Creatinine (mg/dL):", 1.0, key="egfr_s")
        age = st.number_input("Age:", 50, key="egfr_a")
        gender = st.selectbox("Gender:", ["Male", "Female"], key="egfr_g")
        if st.button("Calculate eGFR"):
            gfr = calculators.calc_egfr(creatinine, age, gender)
            st.markdown(f"<div class='card'><b>eGFR:</b> {gfr} mL/min/1.73m²</div>", unsafe_allow_html=True)

# ========================
# 5. Lab Interpretation
# ========================
elif menu == "📊 Lab Interpretation":
    st.header("📊 Lab Interpretation & Trends")
    labs_input = st.text_area("Enter lab values in JSON format",
                              placeholder='{"Hb": 13.5, "WBC": 7000, "Creatinine": 1.1}')
    if st.button("Analyze Labs"):
        try:
            lab_data = json.loads(labs_input)
            st.markdown(f"<div class='card'>{lab.interpret_lab_values(lab_data)}</div>", unsafe_allow_html=True)
            
            # Trend chart for example (single point if no historical data)
            df = pd.DataFrame([lab_data], index=[datetime.date.today()])
            st.line_chart(df)

            # AI interpretation
            analysis = ai_engine.get_hybrid_response(
                "Interpret lab data clinically and for patient view:", context_data=lab_data
            )
            st.expander("👨‍⚕️ Clinical Interpretation").markdown(analysis)
            st.expander("🏡 Patient Friendly Explanation").markdown(analysis)

        except Exception:
            st.error("Invalid JSON. Enter valid lab data.")

# ========================
# 6. Image Analysis
# ========================
elif menu == "📸 Image Analysis":
    st.header("📸 AI Visual Analysis")
    uploaded_file = st.file_uploader("Upload X-Ray, CT, or image", type=['png','jpg','jpeg'])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=400)
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                res = ai_engine.get_hybrid_response("Analyze this image medically.", image=image)
                st.expander("👨‍⚕️ Clinical View").markdown(res)
                st.expander("🏡 Patient View").markdown(res)

# ========================
# FOOTER
# ========================
st.markdown("<hr><p style='text-align:center;color:#757575;'>Health Checker 365 © 2025 | Powered by AI</p>", unsafe_allow_html=True)
