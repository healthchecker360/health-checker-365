import plotly.express as px
import pandas as pd
import datetime

def generate_lab_trend_chart(lab_data):
    """
    lab_data: list of dicts with lab results over time
    Example: [{"date": "2025-12-01", "Hb": 13.5, "WBC": 7000}, ...]
    """
    if not lab_data: return None
    df = pd.DataFrame(lab_data)
    df['date'] = pd.to_datetime(df['date'])
    fig = px.line(df, x='date', y=df.columns[1:], markers=True, title="Lab Trend Over Time")
    fig.update_layout(template="plotly_white")
    return fig

def interpret_lab_values(labs):
    """
    Returns a simple interpretation of lab values
    labs: dict { "Hb": 13.5, "WBC": 7000, ...}
    """
    interpretations = []
    for k, v in labs.items():
        if k.lower() == "hb":
            if v < 12: interpretations.append(f"{k}: Low - Possible anemia")
            elif v > 17: interpretations.append(f"{k}: High - Polycythemia")
            else: interpretations.append(f"{k}: Normal")
        elif k.lower() == "wbc":
            if v < 4000: interpretations.append(f"{k}: Low - Leukopenia")
            elif v > 11000: interpretations.append(f"{k}: High - Possible infection")
            else: interpretations.append(f"{k}: Normal")
        else:
            interpretations.append(f"{k}: {v} (No automated interpretation)")
    return "\n".join(interpretations)
