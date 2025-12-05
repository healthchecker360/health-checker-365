import google.generativeai as genai
import config
import json

# Configure Gemini
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are Health Checker 365.
For every question, provide TWO responses:
1. 👨‍⚕️ CLINICAL VIEW (Technical, Dosing, MOA)
2. 🏡 PATIENT VIEW (Simple, Home Care, Red Flags)
"""

def get_hybrid_response(query, image=None, context_data=None):
    if not config.GEMINI_API_KEY:
        return "⚠️ API Key Missing."

    # BUILD PROMPT
    full_prompt = query
    if context_data:
        full_prompt = f"Internal Data: {json.dumps(context_data)}. Query: {query}"

    # --- THE BULLETPROOF LOGIC ---
    try:
        # ATTEMPT 1: Try the latest fast model (Gemini 1.5 Flash)
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
        if image:
            response = model.generate_content([full_prompt, image])
        else:
            response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        # ATTEMPT 2: Fallback to the stable legacy model (Gemini 1.0 Pro) if Flash fails
        try:
            if image:
                # Use Vision model for images
                fallback_model = genai.GenerativeModel('gemini-pro-vision')
                response = fallback_model.generate_content([full_prompt, image])
            else:
                # Use Text model for chat
                fallback_model = genai.GenerativeModel('gemini-pro')
                response = fallback_model.generate_content(full_prompt)
            return response.text
            
        except Exception as e2:
            # If both fail, show the error
            return f"⚠️ System Error: {str(e)}. (Fallback also failed: {str(e2)})"
