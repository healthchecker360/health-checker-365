import google.generativeai as genai
import json
import config


# ------------------------------
# SYSTEM PROMPT
# ------------------------------
SYSTEM_PROMPT = """
You are Health Checker 365 – a clinical-grade medical assistant.

Provide TWO SEPARATE SECTIONS:

-------------------------------------
👨‍⚕️ CLINICAL VIEW (Professional)
-------------------------------------
Use medical terminology.
Include:
- Differential diagnosis
- Key clinical reasoning
- Treatment options (with dose range)
- Mechanism of action (if drugs involved)
- Monitoring parameters
- Drug–drug interactions
- Contraindications
- Red flags
- Evidence-based guidance

-------------------------------------
🏡 PATIENT VIEW (Simple Explanation)
-------------------------------------
Explain in easy, simple language.
Include:
- What the condition is
- Why it happens (simple physiology)
- How it is treated
- Home care advice
- When to seek urgent help
- Expected side effects in simple wording

-------------------------------------
OUTPUT FORMAT (VERY IMPORTANT)
-------------------------------------

Return EXACTLY this structure:

### 👨‍⚕️ Clinical View
- bullet points
- concise, professional, readable
- separate "Treatment", "Warnings", "Monitoring"

### 🏡 Patient View
- short sentences
- simple wording
- easy-to-follow steps
- clear safety advice

-------------------------------------
DO NOT mix clinical and patient info.
DO NOT add extra headings or commentary.
-------------------------------------
"""


# -----------------------------------------
#   AUTO MODEL PICKER  (HIGHLY RELIABLE)
# -----------------------------------------
def _select_best_model():
    try:
        available = [
            m.name for m in genai.list_models()
            if "generateContent" in m.supported_generation_methods
        ]
    except Exception:
        return "models/gemini-1.5-flash"

    # Priority selection
    if "models/gemini-1.5-pro" in available:
        return "models/gemini-1.5-pro"
    if "models/gemini-1.5-flash" in available:
        return "models/gemini-1.5-flash"
    if "models/gemini-pro" in available:
        return "models/gemini-pro"

    return available[0] if available else None



# -----------------------------------------
#      MAIN HYBRID RESPONSE FUNCTION
# -----------------------------------------
def get_hybrid_response(query, image=None, context_data=None):

    if not config.GEMINI_API_KEY:
        return "⚠️ API Key Missing in config.py"

    # Configure Gemini
    genai.configure(api_key=config.GEMINI_API_KEY)

    # Select model automatically
    model_name = _select_best_model()
    if not model_name:
        return "⚠️ No available models for your API key."

    # Build dynamic prompt
    full_prompt = query
    if context_data:
        full_prompt = (
            f"Internal Medical Data: {json.dumps(context_data)}\n"
            f"User Query: {query}"
        )

    try:
        model = genai.GenerativeModel(
            model_name,
            system_instruction=SYSTEM_PROMPT
        )

        if image:
            response = model.generate_content([full_prompt, image])
        else:
            response = model.generate_content(full_prompt)

        final_text = response.text

        # Clean accidental markdown artifacts
        if final_text.strip().startswith("```"):
            final_text = final_text.strip().lstrip("```").rstrip("```")

        return final_text

    except Exception as e:
        return f"⚠️ Error using {model_name}: {str(e)}"
