class Diagnostic:
    def __init__(
        self,
        patient_id,
        temperature,
        answers,
        test_classification=None,
        test_confidence=None,
        top_patient_factors=None,
        eye_image_path=None,
        eye_scan_path=None,
        eye_classification=None,
        eye_confidence=None,
        risk_level=None,
        recommendation=None,
        pdf_path=None,
    ):
        self.patient_id = int(patient_id)
        self.temperature = float(temperature)
        self.answers = list(answers)

        self.test_confidence = (
            float(test_confidence) if test_confidence is not None else None
        )
        self.test_risk_level = test_classification
        self.top_patient_factors = (
            list(top_patient_factors) if top_patient_factors is not None else None
        )
        self.eye_confidence = (
            float(eye_confidence) if eye_confidence is not None else None
        )
        self.risk_level = float(risk_level) if risk_level is not None else None

        self.image_path = eye_image_path
        self.eye_scan_path = eye_scan_path
        self.eye_classification = eye_classification
        self.recommendation = recommendation
        self.pdf_path = pdf_path
