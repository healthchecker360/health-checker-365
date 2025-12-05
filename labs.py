"""
labs.py
--------
Clinical laboratory analyzer module for GEN.AI Medical Assistant.

Supports:
- CBC (Complete Blood Count)
- LFT (Liver Function Test)
- RFT (Renal Function Test)
- Electrolytes

Provides:
- Reference ranges
- Abnormality flags
- Short interpretation / clinical notes
"""

from typing import Dict, Tuple


# ---------------------------------------------------------------------
# CBC NORMAL RANGES (adult)
# ---------------------------------------------------------------------
CBC_NORMALS = {
    "hemoglobin": (13.5, 17.5),  # g/dL males, females 12-16 g/dL
    "hematocrit": (41, 53),      # % males, females 36-46%
    "wbc": (4.0, 11.0),          # x10^9/L
    "platelets": (150, 400),     # x10^9/L
    "mcv": (80, 100),            # fL
    "mch": (27, 33),             # pg
    "mchc": (32, 36),            # g/dL
}


# ---------------------------------------------------------------------
# LFT NORMAL RANGES
# ---------------------------------------------------------------------
LFT_NORMALS = {
    "alt": (7, 56),      # U/L
    "ast": (10, 40),     # U/L
    "alk_phos": (44, 147),  # U/L
    "total_bilirubin": (0.3, 1.2),  # mg/dL
    "albumin": (3.4, 5.4),          # g/dL
    "total_protein": (6.0, 8.3),    # g/dL
}


# ---------------------------------------------------------------------
# RFT NORMAL RANGES
# ---------------------------------------------------------------------
RFT_NORMALS = {
    "creatinine": (0.6, 1.3),  # mg/dL
    "urea": (7, 20),           # mg/dL
    "sodium": (135, 145),      # mmol/L
    "potassium": (3.5, 5.0),   # mmol/L
    "chloride": (98, 107),     # mmol/L
    "bicarbonate": (22, 28),   # mmol/L
}


# ---------------------------------------------------------------------
# GENERIC LAB CHECK FUNCTION
# ---------------------------------------------------------------------
def check_lab(value: float, normal_range: Tuple[float, float]) -> str:
    """
    Check a lab value against normal range.
    Returns:
        "Low", "Normal", or "High"
    """
    low, high = normal_range
    if value < low:
        return "Low 🔵"
    elif value > high:
        return "High 🔴"
    else:
        return "Normal 🟢"


# ---------------------------------------------------------------------
# CBC ANALYZER
# ---------------------------------------------------------------------
def analyze_cbc(results: Dict[str, float]) -> Dict[str, str]:
    """
    Analyze CBC results and return abnormality flags.
    """
    flags = {}
    for param, value in results.items():
        normal_range = CBC_NORMALS.get(param)
        if normal_range:
            flags[param] = check_lab(value, normal_range)
    return flags


# ---------------------------------------------------------------------
# LFT ANALYZER
# ---------------------------------------------------------------------
def analyze_lft(results: Dict[str, float]) -> Dict[str, str]:
    flags = {}
    for param, value in results.items():
        normal_range = LFT_NORMALS.get(param)
        if normal_range:
            flags[param] = check_lab(value, normal_range)
    return flags


# ---------------------------------------------------------------------
# RFT / ELECTROLYTES ANALYZER
# ---------------------------------------------------------------------
def analyze_rft(results: Dict[str, float]) -> Dict[str, str]:
    flags = {}
    for param, value in results.items():
        normal_range = RFT_NORMALS.get(param)
        if normal_range:
            flags[param] = check_lab(value, normal_range)
    return flags


# ---------------------------------------------------------------------
# COMBINED LAB REPORT
# ---------------------------------------------------------------------
def analyze_all_labs(cbc: Dict[str, float] = None,
                     lft: Dict[str, float] = None,
                     rft: Dict[str, float] = None) -> Dict[str, Dict[str, str]]:
    """
    Analyze all labs at once.
    Returns nested dictionary with flags.
    """
    report = {}
    if cbc:
        report["CBC"] = analyze_cbc(cbc)
    if lft:
        report["LFT"] = analyze_lft(lft)
    if rft:
        report["RFT"] = analyze_rft(rft)
    return report
