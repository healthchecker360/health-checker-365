import google.generativeai as genai
import config
import json
from typing import Optional, Union

# Configure Gemini
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)

SYSTEM_PROMPT = config.SYSTEM_PROMPT if hasattr(config, "SYSTEM_PROMPT") else """
You are Health Checker 365.
Provide:
1. 🏡 PATIENT VIEW (Simple)
2. 👨‍⚕️ CLINICAL VIEW (Technical)
"""

def get_hybrid_response(
    query: str,
    image: Optional[Union[str, bytes]] = None,
    context_data: Optional[dict] = None
) -> str:
    if not config.GEMINI_API_KEY:
        return "⚠️ API Key Missing."

    # --- Dynamic Model Selection ---
    target_model_name = "gemini-1.5-flash"
    try:
        valid_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        if "models/gemini-1.5-flash" in valid_models:
            target_model_name = "models/gemini-1.5-flash"
        elif "models/gemini-pro" in valid_models:
            target_model_name = "models/gemini-pro"
        elif valid_models:
            target_model_name = valid_models[0]
        else:
            return "⚠️ CRITICAL ERROR: No available models for this API key."
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

    # --- Prepare Prompt ---
    full_prompt = query
    if context_data:
        try:
            full_prompt = f"Internal Data: {json.dumps(context_data)}. Query: {query}"
        except Exception:
            full_prompt = query  # fallback if context_data is not serializable

    # --- Generate Response ---
    try:
        model = genai.GenerativeModel(target_model_name, system_instruction=SYSTEM_PROMPT)
        if image:
            response = model.generate_content([full_prompt, image])
        else:
            response = model.generate_content(full_prompt)
        return getattr(response, "text", str(response))
    except Exception as e:
        return f"⚠️ Model Error '{target_model_name}': {str(e)}"
