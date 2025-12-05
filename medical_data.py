"""
medical_data.py
----------------
Local BNF-style Drug Reference Module for GEN.AI Medical Assistant.

This module contains:
- A structured mini-BNF drug database
- Exact drug lookup
- Partial keyword-based search
- Type-safe return values
- Easily expandable architecture

You can later replace/extend this with:
- External JSON database
- RxNorm / OpenFDA / MHRA API integration
"""

from typing import Dict, List, Optional


# ---------------------------------------------------------------------
# INTERNAL MINI-BNF DATABASE
# ---------------------------------------------------------------------
BNF_DATA: Dict[str, Dict[str, str | List[str]]] = {
    "amoxicillin": {
        "class": "Antibiotic (Penicillin)",
        "moa": "Inhibits bacterial cell wall synthesis by binding to PBPs.",
        "dose": "Adult: 500 mg TDS. Child: 125–250 mg TDS.",
        "warnings": "Contraindicated in penicillin allergy. Reduce dose if eGFR < 30.",
        "side_effects": "Rash, diarrhea, hypersensitivity reactions.",
        "formulations": ["Capsule 250mg/500mg", "Suspension 125mg/5ml"],
        "industry": "Store below 25°C. Hygroscopic powder."
    },
    "paracetamol": {
        "class": "Analgesic & Antipyretic",
        "moa": "Inhibits central COX enzymes, elevating pain threshold.",
        "dose": "Adult: 1 g every 4–6 h (max 4 g/day). Child: 15 mg/kg/dose.",
        "warnings": "Hepatotoxic in overdose. Avoid in severe hepatic impairment.",
        "side_effects": "Rare: rash, liver injury in overdose.",
        "formulations": ["Tablet 500mg", "IV infusion 10mg/ml"],
        "industry": "Stable crystalline powder."
    },
    "metformin": {
        "class": "Antidiabetic (Biguanide)",
        "moa": "Reduces hepatic gluconeogenesis and improves insulin sensitivity.",
        "dose": "500 mg BD with meals. Max 2 g/day.",
        "warnings": "Stop if eGFR < 30. Risk of lactic acidosis.",
        "side_effects": "GI upset, B12 deficiency in long-term use.",
        "formulations": ["Tablet 500mg/850mg", "XR 500mg/1000mg"],
        "industry": "Stable solid oral dosage form."
    }
}


# ---------------------------------------------------------------------
# EXACT MATCH LOOKUP
# ---------------------------------------------------------------------
def get_drug_data(name: str) -> Optional[Dict]:
    """
    Returns structured drug information for an exact name match.

    Parameters:
        name (str): Drug name (case-insensitive)

    Returns:
        dict | None: Drug details if found, else None
    """
    if not name:
        return None

    return BNF_DATA.get(name.lower().strip())


# ---------------------------------------------------------------------
# PARTIAL SEARCH (USER-FRIENDLY)
# ---------------------------------------------------------------------
def search_drug(keyword: str) -> List[str]:
    """
    Returns drugs that match keyword partially.
    Example:
        input: "amo"
        output: ["amoxicillin"]

    Parameters:
        keyword (str): Search text

    Returns:
        list[str]: List of matching drug names
    """
    if not keyword:
        return []

    key = keyword.lower().strip()
    return [drug for drug in BNF_DATA if key in drug]


# ---------------------------------------------------------------------
# LIST ALL DRUGS (optional utility)
# ---------------------------------------------------------------------
def list_all_drugs() -> List[str]:
    """
    Returns a list of all drugs available in the local database.
    """
    return list(BNF_DATA.keys())
