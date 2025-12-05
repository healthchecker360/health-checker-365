import streamlit as st
import config
import ai_engine
import medical_data
import calculators
from PIL import Image

st.set_page_config(layout="wide", page_title=config.APP_NAME, page_icon="🏥")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏥 Health Checker 365")
    
    # Check if Key is present
    if not config.GEMINI_API_KEY:
        st.error("⚠️ API Key not detected! Add it to Streamlit Secrets.")
    
    menu = st.radio("Modules", [
        "1. 💬 Chat & Diagnosis", 
        "2. 💊 Drug Module", 
        "3. 🧮 Calculators", 
        "4. 📸 Image Analysis"
    ])

# --- 1. CHAT ---
if menu == "1. 💬 Chat & Diagnosis":
    st.title("💬 AI Clinical Chat")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Describe symptoms..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                res = ai_engine.get_hybrid_response(prompt)
                st.markdown(res)
        st.session_state.messages.append({"role": "assistant", "content": res})

# --- 2. DRUG MODULE ---
elif menu == "2. 💊 Drug Module":
    st.title("💊 Drug Database")
    drug = st.text_input("Enter Drug Name:")
    if st.button("Search Monograph"):
        internal = medical_data.get_drug_data(drug)
        if internal: st.success("Found in Internal BNF")
        
        with st.spinner("Generating Dual-View Monograph..."):
            res = ai_engine.get_hybrid_response(f"Monograph for {drug}", context_data=internal)
            st.markdown(res)

# --- 3. CALCULATORS ---
elif menu == "3. 🧮 Calculators":
    st.title("🧮 Medical Calculators")
    tabs = st.tabs(["BMI", "eGFR"])
    
    with tabs[0]:
        w = st.number_input("Weight (kg)", 70.0)
        h = st.number_input("Height (cm)", 175.0)
        if st.button("Calc BMI"):
            val, cat = calculators.calc_bmi(w, h)
            st.metric("BMI", val, cat)
            
    with tabs[1]:
        scr = st.number_input("Creatinine", 1.0)
        age = st.number_input("Age", 50)
        gen = st.selectbox("Gender", ["Male", "Female"])
        if st.button("Calc eGFR"):
            st.metric("eGFR", calculators.calc_egfr(scr, age, gen))

# --- 4. IMAGE ANALYSIS ---
elif menu == "4. 📸 Image Analysis":
    st.title("📸 Visual Diagnosis")
    up_file = st.file_uploader("Upload X-Ray/Rx", type=['png','jpg','jpeg'])
    
    if up_file:
        img = Image.open(up_file)
        st.image(img, width=300)
        if st.button("Analyze"):
            with st.spinner("Scanning..."):
                res = ai_engine.get_hybrid_response("Analyze this image.", image=img)
                st.markdown(res)
