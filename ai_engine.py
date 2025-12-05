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

    try:
        # UPDATED: Use 'gemini-1.5-flash-latest' which maps to the newest stable version
        # If this fails, the code below catches it.
        model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=SYSTEM_PROMPT)
        
        if image:
            response = model.generate_content([full_prompt, image])
        else:
            response = model.generate_content(full_prompt)
            
        return response.text
        
    except Exception as e:
        # Fallback Error Message
        return f"⚠️ AI Error: {str(e)}. \n\n*Tip: Check that 'Generative Language API' is enabled in your Google Cloud Console.*"
