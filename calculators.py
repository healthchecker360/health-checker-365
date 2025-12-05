"""
calculators.py
---------------
Clinical & pharmaceutical calculators for GEN.AI Medical Assistant.

Includes:
- BMI
- eGFR (CKD-EPI 2021)
- Creatinine Clearance (Cockcroft-Gault)
- BSA (DuBois)
- Dose by Weight
- Dose by BSA
- IV Drip Rate
- Adjusted Body Weight
- Anion Gap
- Corrected Calcium
- Pediatric Dose (Young / Clark / Fried)
- Insulin Sensitivity Factor (ISF)
- A-a Gradient (Respiratory)
"""

import math


# ---------------------------------------------------------------------
# BMI
# ---------------------------------------------------------------------
def calc_bmi(weight, height):
    if not height or height <= 0:
        return 0, "Error"

    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        status = "Underweight 🔵"
    elif bmi < 25:
        status = "Normal 🟢"
    elif bmi < 30:
        status = "Overweight 🟠"
    else:
        status = "Obese 🔴"

    return round(bmi, 2), status


# ---------------------------------------------------------------------
# eGFR – CKD-EPI 2021
# ---------------------------------------------------------------------
def calc_egfr(scr, age, gender):
    try:
        k = 0.7 if gender == "Female" else 0.9
        a = -0.329 if gender == "Female" else -0.411
        f = 1.018 if gender == "Female" else 1

        gfr = 142 * (min(scr / k, 1) ** a) * (max(scr / k, 1) ** -1.200) * (0.9938 ** age) * f
        return round(gfr, 1)
    except:
        return 0


# ---------------------------------------------------------------------
# Creatinine Clearance – Cockcroft-Gault
# ---------------------------------------------------------------------
def calc_crcl(weight, age, scr, gender):
    try:
        crcl = ((140 - age) * weight) / (72 * scr)
        if gender == "Female":
            crcl *= 0.85
        return round(crcl, 1)
    except:
        return 0


# ---------------------------------------------------------------------
# Body Surface Area – DuBois
# ---------------------------------------------------------------------
def calc_bsa(weight, height):
    try:
        bsa = 0.007184 * (weight ** 0.425) * (height ** 0.725)
        return round(bsa, 2)
    except:
        return 0


# ---------------------------------------------------------------------
# Dose by Weight (mg/kg)
# ---------------------------------------------------------------------
def calc_weight_dose(weight, mg_per_kg):
    try:
        dose = weight * mg_per_kg
        return round(dose, 2)
    except:
        return 0


# ---------------------------------------------------------------------
# Dose by BSA (mg/m²)
# ---------------------------------------------------------------------
def calc_bsa_dose(bsa, mg_per_m2):
    try:
        return round(bsa * mg_per_m2, 2)
    except:
        return 0


# ---------------------------------------------------------------------
# Adjusted Body Weight (Obesity Dosing)
# ---------------------------------------------------------------------
def calc_adjusted_weight(actual, ideal):
    try:
        return round(ideal + 0.4 * (actual - ideal), 2)
    except:
        return 0


# ---------------------------------------------------------------------
# IV Drip Calculator (drops/min)
# ---------------------------------------------------------------------
def calc_iv_drip(volume_ml, time_min, drop_factor=20):
    try:
        rate = (volume_ml * drop_factor) / time_min
        return round(rate, 1)
    except:
        return 0


# ---------------------------------------------------------------------
# Anion Gap
# ---------------------------------------------------------------------
def calc_anion_gap(na, cl, hco3):
    try:
        return na - (cl + hco3)
    except:
        return 0


# ---------------------------------------------------------------------
# Corrected Calcium (for hypoalbuminemia)
# ---------------------------------------------------------------------
def calc_corrected_calcium(total_ca, albumin):
    try:
        corrected = total_ca + 0.8 * (4 - albumin)
        return round(corrected, 2)
    except:
        return 0


# ---------------------------------------------------------------------
# Pediatric Dosing
# ---------------------------------------------------------------------
def calc_clarks_rule(weight_kg, adult_dose):
    """Child dose = (weight (kg) / 70) × adult dose"""
    try:
        return round((weight_kg / 70) * adult_dose, 2)
    except:
        return 0


def calc_youngs_rule(age, adult_dose):
    """(Age / (Age + 12)) × adult dose"""
    try:
        return round((age / (age + 12)) * adult_dose, 2)
    except:
        return 0


def calc_frieds_rule(age_months, adult_dose):
    """(Age in months / 150) × adult dose"""
    try:
        return round((age_months / 150) * adult_dose, 2)
    except:
        return 0


# ---------------------------------------------------------------------
# Insulin Sensitivity Factor (ISF) – 1800 Rule
# ---------------------------------------------------------------------
def calc_isf(tdd):
    """ISF = 1800 / total daily insulin dose"""
    try:
        return round(1800 / tdd, 1)
    except:
        return 0


# ---------------------------------------------------------------------
# A–a Gradient
# ---------------------------------------------------------------------
def calc_aagradient(fiO2, paO2, paCO2):
    """A–a gradient = (FiO2 × 713) – (PaCO2 / 0.8) – PaO2"""
    try:
        aa = (fiO2 * 713) - (paCO2 / 0.8) - paO2
        return round(aa, 1)
    except:
        return 0
