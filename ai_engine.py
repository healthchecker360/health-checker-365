import google.generativeai as genai
import config
import json

# Configure Gemini using the secure key from config
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

# THE DUAL-VIEW PROMPT
SYSTEM_PROMPT = """
You are Health Checker 365.
For every question, provide TWO responses:

1. 👨‍⚕️ **CLINICAL VIEW** (For Doctors):
   - Medical terms, MOA, Dosing guidelines, Interactions.
   
2. 🏡 **PATIENT VIEW** (For Users):
   - Simple 5th-grade language.
   - 'How to take', 'What to avoid', 'When to call a doctor'.

If looking up a drug, check Internal Data first.
If diagnosing, give Differentials and Red Flags.
"""

def get_hybrid_response(query, image=None, context_data=None):
    # Safety Check: Ensure Key exists
    if not config.GEMINI_API_KEY:
        return "⚠️ API Key Missing. Please set it in Streamlit Secrets."

    # BUILD THE PROMPT
    full_prompt = query
    
    # If we found data in medical_data.py, add it to the prompt
    if context_data:
        full_prompt = f"Internal Data Found: {json.dumps(context_data)}. Use this data primarily. Query: {query}"

    try:
        # Initialize the Model (Without the Search Tool to prevent errors)
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
        
        # Generate Content
        if image:
            response = model.generate_content([full_prompt, image])
        else:
            response = model.generate_content(full_prompt)
            
        return response.text
        
    except Exception as e:
        return f"⚠️ System Error: {str(e)}"
