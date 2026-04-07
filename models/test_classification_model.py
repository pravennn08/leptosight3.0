import joblib
import numpy as np
import os
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "test_model.pkl")


class TestClassificationModel:

    def __init__(self):
        self.model = None
        self.labels = {0: "Safe", 1: "Mild", 2: "Moderate", 3: "Severe"}
        self.features = [
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

    def load(self):
        if self.model is None:
            self.model = joblib.load(MODEL_PATH)
        return self.model

    def top_features(self, n=5):

        model = self.load()

        importance = model.feature_importances_

        pairs = list(zip(self.features, importance))

        pairs.sort(key=lambda x: x[1], reverse=True)

        return [(f, round(i * 100, 2)) for f, i in pairs[:n]]

    def patient_factors(self, data, n=5):

        model = self.load()

        importances = np.array(model.feature_importances_)

        patient_values = np.array(data[0], dtype=float)

        # Contribution score
        scores = patient_values * importances

        contributions = list(zip(self.features, scores))

        # Sort highest contribution first
        contributions.sort(key=lambda x: x[1], reverse=True)

        return contributions[:n]

    def predict(self, data):

        model = self.load()
        data_df = pd.DataFrame(data, columns=self.features)
        prediction = model.predict(data_df)[0]
        probabilities = model.predict_proba(data_df)[0]
        confidence = float(max(probabilities))
        prob_percent = [round(float(p) * 100, 2) for p in probabilities]

        return {
            "classification": self.labels[prediction],
            "prediction": int(prediction),
            "confidence": round(confidence * 100, 2),
            "probabilities": {
                self.labels[i]: prob_percent[i] for i in range(len(prob_percent))
            },
            "top_global_factors": self.top_features(),
            "top_patient_factors": self.patient_factors(data),
        }
