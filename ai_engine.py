import google.generativeai as genai
import config
import json

# Configure Gemini
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are Health Checker 365.
Provide:
1. 👨‍⚕️ CLINICAL VIEW (Technical)
2. 🏡 PATIENT VIEW (Simple)
"""

def get_hybrid_response(query, image=None, context_data=None):
    if not config.GEMINI_API_KEY:
        return "⚠️ API Key Missing."

    # --- DYNAMIC MODEL SELECTOR (The Fix) ---
    # This block asks Google what models are actually available to your key
    target_model_name = 'gemini-1.5-flash' # Default hope
    try:
        valid_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Logic to pick the best available model
        if 'models/gemini-1.5-flash' in valid_models:
            target_model_name = 'models/gemini-1.5-flash'
        elif 'models/gemini-pro' in valid_models:
            target_model_name = 'models/gemini-pro'
        elif len(valid_models) > 0:
            target_model_name = valid_models[0] # Pick the first working model found
        else:
            return "⚠️ CRITICAL ERROR: Your API Key has access to 0 models. Please generate a new key at aistudio.google.com"
            
    except Exception as e:
        return f"⚠️ Connection Error: Could not list models. Check if your API Key is valid. Error: {str(e)}"

    # --- GENERATION ---
    full_prompt = query
    if context_data:
        full_prompt = f"Internal Data: {json.dumps(context_data)}. Query: {query}"

    try:
        # Use the model we found above
        model = genai.GenerativeModel(target_model_name, system_instruction=SYSTEM_PROMPT)
        
        if image:
            response = model.generate_content([full_prompt, image])
        else:
            response = model.generate_content(full_prompt)
            
        return response.text
        
    except Exception as e:
        return f"⚠️ Final Error using model '{target_model_name}': {str(e)}"
