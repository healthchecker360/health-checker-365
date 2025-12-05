"""
config.py
---------
Central configuration module for GEN.AI Medical Assistant.

Handles:
- App-level constants
- Secure API key loading
- Directory initialization
- Theme settings

Streamlit Cloud:
    --> prefers st.secrets for keys
Local development:
    --> uses environment variables
"""

import os
import streamlit as st


# ---------------------------------------------------------------------
# APPLICATION SETTINGS
# ---------------------------------------------------------------------
APP_NAME: str = "Health Checker 365"
THEME_COLOR: str = "#008080"


# ---------------------------------------------------------------------
# API KEYS (Secure Loading)
# ---------------------------------------------------------------------
def load_gemini_key() -> str:
    """
    Loads Gemini API Key from Streamlit Secrets (preferred)
    or from local environment variables.

    Returns:
        str: Gemini API Key

    Raises:
        RuntimeError: If no key is found.
    """
    key = None

    # Try Streamlit Secrets (Cloud deployment)
    try:
        key = st.secrets.get("GEMINI_API_KEY", None)
    except Exception:
        key = None

    # Try Environment Variable (Local development)
    if not key:
        key = os.getenv("GEMINI_API_KEY")

    if not key:
        raise RuntimeError(
            "❌ Gemini API Key missing. "
            "Add GEMINI_API_KEY in Streamlit secrets or environment variables."
        )

    return key


# Load the key once globally
GEMINI_API_KEY = load_gemini_key()


# ---------------------------------------------------------------------
# STORAGE AND DIRECTORIES
# ---------------------------------------------------------------------
BASE_DIR = "data"
TEMP_DIR = os.path.join(BASE_DIR, "temp")
USER_DATA_DIR = os.path.join(BASE_DIR, "user_records")

# Create directories if missing
for path in [BASE_DIR, TEMP_DIR, USER_DATA_DIR]:
    if not os.path.exists(path):
        os.makedirs(path)


# ---------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------
def get_storage_paths() -> dict:
    """
    Returns standard storage directory paths.
    Useful for other modules.
    """
    return {
        "base": BASE_DIR,
        "temp": TEMP_DIR,
        "user_data": USER_DATA_DIR,
    }
