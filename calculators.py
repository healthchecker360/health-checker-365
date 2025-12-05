def calc_bmi(weight, height):
    if not height: return 0, "Error"
    bmi = weight / ((height/100)**2)
    if bmi < 18.5: return round(bmi,2), "Underweight 🔵"
    if bmi < 25: return round(bmi,2), "Normal 🟢"
    if bmi < 30: return round(bmi,2), "Overweight 🟠"
    return round(bmi,2), "Obese 🔴"

def calc_egfr(scr, age, gender):
    # CKD-EPI 2021 Formula
    try:
        k = 0.7 if gender == "Female" else 0.9
        a = -0.329 if gender == "Female" else -0.411
        f = 1.018 if gender == "Female" else 1
        gfr = 142 * (min(scr/k, 1)**a) * (max(scr/k, 1)**-1.200) * (0.9938**age) * f
        return round(gfr, 1)
    except: return 0
