import streamlit as st
import os

# SETTINGS
APP_NAME = "Health Checker 365"
THEME_COLOR = "#008080"

# SECURE KEY HANDLING
# This tries to get the key from Streamlit Secrets (Cloud) or Environment (Local)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# STORAGE
# Note: Streamlit Cloud does not have persistent Google Drive storage.
# We will use temporary local storage for this session.
BASE_DIR = "data"
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)
