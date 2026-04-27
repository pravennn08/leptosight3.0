import joblib
import pandas as pd
import shap
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "custom.pkl")

MODEL = joblib.load(MODEL_PATH)
EXPLAINER = shap.TreeExplainer(MODEL)


class TestClassificationModel:

    def __init__(self):
        self.model = MODEL
        self.labels = {0: "Safe", 1: "Mild", 2: "Moderate", 3: "Severe"}

        # must match training order EXACTLY
        self.columns = [
            "flood_exposure",
            "wounds",
            "environment",
            "illness_start",
            "body_condition",
            "headache_freq",
            "headache_intensity",
            "appetite_change",
            "nausea",
            "vomiting",
            "skin_changes",
            "eye_changes",
            "light_sensitivity",
            "abdominal_press",
            "bowel_change",
            "abdominal_movement",
            "fatigue_activity",
            "energy_level",
            "calf_pain",
            "leg_feeling",
            "temperature",
        ]

    # -----------------------------------
    # 🔥 TOP 5 FACTORS (UI READY)
    # -----------------------------------
    def top_contributing_features(self, data, pred):

        shap_values = EXPLAINER(data)

        values = shap_values.values[0][:, pred]

        importance = pd.Series(values, index=self.columns).sort_values(
            key=abs, ascending=False
        )

        top5 = []

        for feature, val in importance.head(5).items():
            top5.append(
                {
                    "feature": feature,
                    # "effect": "supports" if val > 0 else "opposes",
                    "score": round(float(val), 3),
                }
            )

        return top5

    # -----------------------------------
    # 🔥 MAIN PREDICT FUNCTION
    # -----------------------------------
    def predict(self, data):

        # Convert input → DataFrame (VERY IMPORTANT)
        df = pd.DataFrame(data, columns=self.columns)

        # Prediction
        pred = self.model.predict(df)[0]

        # Confidence
        probs = self.model.predict_proba(df)[0]
        confidence = probs[pred]

        # Top factors
        top_factors = self.top_contributing_features(df, pred)

        return {
            "classification": self.labels[pred],
            "prediction": int(pred),
            "confidence": round(confidence * 100, 2),
            "top_patient_factors": top_factors,
        }
