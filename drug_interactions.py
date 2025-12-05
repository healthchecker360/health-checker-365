"""
drug_interactions.py
--------------------
Drug–Drug Interaction Checker for GEN.AI Medical Assistant.

Features:
- Input: List of drugs
- Output: Interactions with severity and clinical notes
- Internal database for common interactions
- Expandable for large BNF / RxNorm API integration
"""

from typing import List, Dict, Tuple

# ---------------------------------------------------------------------
# INTERNAL DRUG INTERACTION DATABASE
# ---------------------------------------------------------------------
# Example structure: (drug1, drug2): {severity, note}
INTERACTION_DB: Dict[Tuple[str, str], Dict[str, str]] = {
    ("warfarin", "amoxicillin"): {
        "severity": "Moderate ⚠️",
        "note": "Amoxicillin may increase bleeding risk by altering gut flora affecting vitamin K."
    },
    ("metformin", "contrast dye"): {
        "severity": "Severe 🔴",
        "note": "Risk of lactic acidosis. Hold metformin 48h before and after contrast if eGFR < 60."
    },
    ("aspirin", "ibuprofen"): {
        "severity": "Moderate ⚠️",
        "note": "Ibuprofen may reduce cardioprotective effect of aspirin."
    },
    ("lisinopril", "spironolactone"): {
        "severity": "Severe 🔴",
        "note": "Combined risk of hyperkalemia and hypotension."
    },
    ("simvastatin", "clarithromycin"): {
        "severity": "Severe 🔴",
        "note": "Increased risk of rhabdomyolysis due to CYP3A4 inhibition."
    },
    ("digoxin", "furosemide"): {
        "severity": "Moderate ⚠️",
        "note": "Furosemide-induced hypokalemia increases risk of digoxin toxicity."
    }
}


# ---------------------------------------------------------------------
# INTERACTION CHECK FUNCTION
# ---------------------------------------------------------------------
def check_interactions(drug_list: List[str]) -> List[Dict[str, str]]:
    """
    Checks a list of drugs for known interactions.

    Parameters:
        drug_list (list[str]): List of drug names

    Returns:
        list of dict: Each dict contains:
            drug1, drug2, severity, note
    """
    interactions_found = []
    drugs = [d.lower().strip() for d in drug_list]

    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            pair = (drugs[i], drugs[j])
            reverse_pair = (drugs[j], drugs[i])

            if pair in INTERACTION_DB:
                entry = INTERACTION_DB[pair]
                interactions_found.append({
                    "drug1": drugs[i],
                    "drug2": drugs[j],
                    "severity": entry["severity"],
                    "note": entry["note"]
                })
            elif reverse_pair in INTERACTION_DB:
                entry = INTERACTION_DB[reverse_pair]
                interactions_found.append({
                    "drug1": drugs[j],
                    "drug2": drugs[i],
                    "severity": entry["severity"],
                    "note": entry["note"]
                })

    return interactions_found


# ---------------------------------------------------------------------
# UTILITY FUNCTION TO ADD NEW INTERACTION
# ---------------------------------------------------------------------
def add_interaction(drug1: str, drug2: str, severity: str, note: str) -> None:
    """
    Adds a new drug-drug interaction to the database.
    """
    INTERACTION_DB[(drug1.lower().strip(), drug2.lower().strip())] = {
        "severity": severity,
        "note": note
    }


# ---------------------------------------------------------------------
# UTILITY FUNCTION TO LIST ALL KNOWN INTERACTIONS
# ---------------------------------------------------------------------
def list_all_interactions() -> List[Tuple[str, str]]:
    """
    Returns a list of all drug pairs in the internal database.
    """
    return list(INTERACTION_DB.keys())
