import json

# --- INTERNAL BNF DATABASE ---
# 📝 EDIT HERE: Add more drugs to this dictionary manually.
BNF_DATA = {
    "amoxicillin": {
        "class": "Antibiotic (Penicillin)",
        "dose": "Adult: 500mg TDS. Child: 125-250mg TDS.",
        "warnings": "Contraindicated in Penicillin Allergy. Reduce dose if eGFR < 30.",
        "formulations": ["Capsule 250mg/500mg", "Suspension 125mg/5ml"],
        "industry": "Store < 25C. Hygroscopic powder."
    },
    "paracetamol": {
        "class": "Analgesic",
        "dose": "Adult: 1g every 4-6h. Max 4g/day.",
        "warnings": "Hepatotoxicity in overdose.",
        "formulations": ["Tablet 500mg", "IV Infusion 10mg/ml"],
        "industry": "Stable crystalline powder."
    },
    "metformin": {
        "class": "Biguanide (Antidiabetic)",
        "dose": "500mg BD with meals. Max 2g/day.",
        "warnings": "Stop if eGFR < 30. Risk of Lactic Acidosis.",
        "formulations": ["Tablet 500mg/850mg", "XR 500mg/1000mg"]
    }
}

def get_drug_data(name):
    return BNF_DATA.get(name.lower().strip(), None)
