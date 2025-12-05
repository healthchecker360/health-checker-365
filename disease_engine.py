"""
disease_engine.py
-----------------
Symptom-to-Diagnosis engine for GEN.AI Medical Assistant.

Features:
- Input: List of symptoms
- Output: Possible diagnoses with probability scores
- Rule-based scoring (can integrate ML/AI later)
- Expandable database for diseases
"""

from typing import List, Dict, Tuple


# ---------------------------------------------------------------------
# INTERNAL DISEASE DATABASE
# ---------------------------------------------------------------------
# Each disease has a list of key symptoms (simplified example)
DISEASE_DB: Dict[str, List[str]] = {
    "Common Cold": ["sneezing", "runny nose", "sore throat", "cough", "mild fever"],
    "Influenza": ["high fever", "cough", "sore throat", "body ache", "fatigue", "headache"],
    "COVID-19": ["fever", "dry cough", "fatigue", "loss of taste", "loss of smell", "difficulty breathing"],
    "Urinary Tract Infection": ["dysuria", "frequency", "urgency", "lower abdominal pain", "hematuria"],
    "Diabetes Mellitus": ["polyuria", "polydipsia", "polyphagia", "fatigue", "blurred vision"],
    "Hypertension": ["headache", "dizziness", "blurred vision", "nosebleed", "fatigue"],
    "Pneumonia": ["fever", "cough", "shortness of breath", "chest pain", "fatigue", "chills"]
}


# ---------------------------------------------------------------------
# SCORING FUNCTION
# ---------------------------------------------------------------------
def calculate_probability(symptoms: List[str], disease_symptoms: List[str]) -> float:
    """
    Returns probability score (0-100%) based on symptom match.
    """
    if not disease_symptoms:
        return 0.0

    matches = sum(1 for s in symptoms if s.lower().strip() in [d.lower() for d in disease_symptoms])
    probability = (matches / len(disease_symptoms)) * 100
    return round(probability, 1)


# ---------------------------------------------------------------------
# DIAGNOSIS FUNCTION
# ---------------------------------------------------------------------
def diagnose(symptoms: List[str], top_n: int = 3) -> List[Tuple[str, float]]:
    """
    Returns a list of possible diagnoses with probability scores.
    
    Parameters:
        symptoms (list[str]): List of input symptoms
        top_n (int): Number of top probable diseases to return
    
    Returns:
        list of tuples: [(disease_name, probability%), ...]
    """
    if not symptoms:
        return []

    disease_probs = []
    for disease, disease_symptoms in DISEASE_DB.items():
        prob = calculate_probability(symptoms, disease_symptoms)
        if prob > 0:
            disease_probs.append((disease, prob))

    # Sort by probability descending
    disease_probs.sort(key=lambda x: x[1], reverse=True)

    # Return top_n results
    return disease_probs[:top_n]


# ---------------------------------------------------------------------
# UTILITY FUNCTION TO ADD NEW DISEASE
# ---------------------------------------------------------------------
def add_disease(name: str, symptoms: List[str]) -> None:
    """
    Adds a new disease to the internal database.
    """
    DISEASE_DB[name] = symptoms


# ---------------------------------------------------------------------
# UTILITY FUNCTION TO LIST ALL DISEASES
# ---------------------------------------------------------------------
def list_all_diseases() -> List[str]:
    """
    Returns list of all diseases in the internal database.
    """
    return list(DISEASE_DB.keys())
