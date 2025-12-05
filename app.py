import streamlit as st
import config
import ai_engine
import medical_data
import calculators
import drug_interactions
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(
    page_title=config.APP_NAME,
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
st.markdown("""
<style>
body {background-color: #f0f2f6;}
h1, h2, h3, h4, h5 {color: #008080;}
.stButton>button {background-color: #008080; color: white; border-radius: 8px; border: none; padding: 8px 16px;}
.stButton>button:hover {background-color: #006666; color: white;}
.stSidebar {background-color: #e0f2f2;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏥 Health Checker 365")
    st.write("Your AI Medical Assistant")

    if not config.GEMINI_API_KEY:
        st.error("⚠️ API Key missing! Add it to Streamlit Secrets or .env file.")

    menu = st.radio(
        "Select Module",
        [
            "💬 Chat & Diagnosis",
            "💊 Drug Module",
            "💉 Drug Interactions",
            "🧮 Calculators",
            "📊 Lab Interpretation",
            "📸 Image Analysis"
        ]
    )

# -------------------
# 1. CHAT & DIAGNOSIS
# -------------------
if menu == "💬 Chat & Diagnosis":
    st.header("💬 AI Clinical Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Describe your symptoms or medical query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI analyzing..."):
                res = ai_engine.get_hybrid_response(prompt)
                st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# -------------------
# 2. DRUG MODULE
# -------------------
elif menu == "💊 Drug Module":
    st.header("💊 Drug Information Module")
    drug = st.text_input("Enter Drug Name:")

    if st.button("Search Drug"):
        internal_data = medical_data.get_drug_data(drug)
        if internal_data:
            st.success("✅ Found in Internal BNF Database")
        else:
            st.warning("⚠️ Drug not found internally. Fetching AI-generated monograph...")

        with st.spinner("Generating dual-view monograph..."):
            res = ai_engine.get_hybrid_response(
                f"Provide a dual-view monograph for {drug}.",
                context_data=internal_data
            )
            st.markdown(res)

# -------------------
# 3. DRUG INTERACTIONS
# -------------------
elif menu == "💉 Drug Interactions":
    st.header("⚠️ Drug Interaction Checker")
    drugs_input = st.text_area(
        "Enter drug names separated by commas:",
        placeholder="e.g., warfarin, amoxicillin, aspirin"
    )

    if st.button("Check Interactions"):
        drug_list = [d.strip() for d in drugs_input.split(",") if d.strip()]
        interactions = drug_interactions.check_interactions(drug_list)
        if interactions:
            for inter in interactions:
                st.markdown(
                    f"**{inter['drug1'].title()} + {inter['drug2'].title()}** → "
                    f"{inter['severity']}\n\n{inter['note']}"
                )
        else:
            st.success("No known interactions found among listed drugs.")

# -------------------
# 4. CALCULATORS
# -------------------
elif menu == "🧮 Calculators":
    st.header("🧮 Medical Calculators")
    tabs = st.tabs(["BMI", "eGFR"])

    with tabs[0]:
        st.subheader("Body Mass Index (BMI)")
        weight = st.number_input("Weight (kg):", 70.0)
        height = st.number_input("Height (cm):", 175.0)
        if st.button("Calculate BMI", key="bmi_calc"):
            val, cat = calculators.calc_bmi(weight, height)
            st.metric(label="BMI", value=val, delta=cat)

    with tabs[1]:
        st.subheader("Estimated GFR (CKD-EPI)")
        creatinine = st.number_input("Serum Creatinine (mg/dL):", 1.0)
        age = st.number_input("Age:", 50)
        gender = st.selectbox("Gender:", ["Male", "Female"])
        if st.button("Calculate eGFR", key="egfr_calc"):
            gfr = calculators.calc_egfr(creatinine, age, gender)
            st.metric(label="eGFR (mL/min/1.73m²)", value=gfr)

# -------------------
# 5. LAB INTERPRETATION (Placeholder)
# -------------------
elif menu == "📊 Lab Interpretation":
    st.header("📊 Lab Interpretation")
    st.info("This module will analyze lab results and provide guidance.")
    labs_input = st.text_area(
        "Enter lab values in JSON format:",
        placeholder='{"Hb": 13.5, "WBC": 7000, "Creatinine": 1.1}'
    )
    if st.button("Analyze Labs"):
        try:
            lab_data = json.loads(labs_input)
            st.success("Lab data received. AI analysis coming soon...")
            analysis = ai_engine.get_hybrid_response(
                "Interpret the following lab data clinically and for patient view:",
                context_data=lab_data
            )
            st.markdown(analysis)
        except Exception:
            st.error("Invalid JSON format. Please enter valid JSON.")

# -------------------
# 6. IMAGE ANALYSIS
# -------------------
elif menu == "📸 Image Analysis":
    st.header("📸 AI Visual Analysis")
    uploaded_file = st.file_uploader("Upload X-Ray, CT, or Image file", type=['png','jpg','jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=400)
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                res = ai_engine.get_hybrid_response("Analyze this image medically.", image=image)
                st.markdown(res)

# -------------------
# FOOTER
# -------------------
st.markdown("<hr><p style='text-align:center;'>Health Checker 365 © 2025 | Powered by AI</p>", unsafe_allow_html=True)
